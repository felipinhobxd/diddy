import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

database_url = os.environ.get('DATABASE_URL')
if database_url:
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Initialize DB within app context
with app.app_context():
    db.create_all()

def login_user(user):
    session.clear()
    session['user_id'] = user.id

def logout_user():
    session.clear()

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not get_current_user():
            return redirect(url_for('login_page'))
        return fn(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    user = get_current_user()
    if user:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/login')
def login_page():
    if get_current_user():
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register_page():
    if get_current_user():
        return redirect(url_for('dashboard'))
    return render_template('cadastro.html')

@app.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    return render_template('dashboard.html', email=user.email)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'success': False, 'message': 'Preencha todos os campos.'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'success': False, 'message': 'Esta conta já existe.'}), 409
    password_hash = generate_password_hash(password)
    user = User(email=email, password_hash=password_hash)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Esta conta já existe.'}), 409
    # Redirect to login page after registration
    return jsonify({'success': True, 'message': 'Cadastro realizado com sucesso!', 'redirect': url_for('login_page')}), 201

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'success': False, 'message': 'Preencha todos os campos.'}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'success': False, 'message': 'Senha incorreta ou a conta não existe.'}), 401
    login_user(user)
    # Redirect to YouTube after successful login
    return jsonify({'success': True, 'redirect': 'https://cdn.vlipsy.com/clips/3hEsFXt9/360p-watermark.mp4?token=v1_f_1750195744_8G1fCZMzo'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
