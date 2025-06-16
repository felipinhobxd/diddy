import pytest
from app import app, db, User

@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def register(client, email, password):
    return client.post('/register', data={'email': email, 'password': password}, follow_redirects=True)

def login(client, email, password):
    return client.post('/login', data={'email': email, 'password': password}, follow_redirects=True)

def test_register_login(client):
    rv = register(client, 'test@example.com', 'Password1')
    assert b'Cadastro realizado com sucesso' in rv.data
    rv = login(client, 'test@example.com', 'Password1')
    assert rv.status_code in (200, 302)
