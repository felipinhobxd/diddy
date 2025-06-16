// Toggle de senha para login e cadastro
document.addEventListener('DOMContentLoaded', () => {
    const togglePwdButtons = document.querySelectorAll('.toggle-password');
    togglePwdButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const wrapper = btn.parentElement;
            const input = wrapper.querySelector('input');
            input.type = (input.type === 'password') ? 'text' : 'password';
        });
    });

    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = loginForm.email.value;
            const password = loginForm.password.value;
            const messageDiv = loginForm.querySelector('#message');
            messageDiv.textContent = '';
            try {
                const res = await fetch('/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await res.json();
                if (data.success) {
                    window.location.href = data.redirect;
                } else {
                    messageDiv.style.color = '#ffbbbb';
                    messageDiv.textContent = data.message;
                }
            } catch (err) {
                messageDiv.style.color = '#ffbbbb';
                messageDiv.textContent = 'Erro na conexão.';
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = registerForm.email.value;
            const password = registerForm.password.value;
            const confirmPassword = registerForm.confirmPassword.value;
            const messageDiv = registerForm.querySelector('#message');
            messageDiv.textContent = '';
            if (password !== confirmPassword) {
                messageDiv.style.color = '#ffbbbb';
                messageDiv.textContent = 'As senhas não coincidem.';
                return;
            }
            try {
                const res = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await res.json();
                if (data.success) {
                    messageDiv.style.color = '#bbffbb';
                    messageDiv.textContent = data.message;
                    setTimeout(() => {
                        window.location.href = data.redirect;
                    }, 1500);
                } else {
                    messageDiv.style.color = '#ffbbbb';
                    messageDiv.textContent = data.message;
                }
            } catch (err) {
                messageDiv.style.color = '#ffbbbb';
                messageDiv.textContent = 'Erro na conexão.';
            }
        });
    }
});
