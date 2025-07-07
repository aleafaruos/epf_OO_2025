
document.addEventListener('DOMContentLoaded', function() {

    // --- LÓGICA PARA O MODAL DE LOGIN ---
    const loginForm = document.querySelector('#loginModal form');
    const loginErrorDiv = document.querySelector('#login-error-message');

    if (loginForm && loginErrorDiv) {
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault(); // Impede o formulário de recarregar a página
            loginErrorDiv.style.display = 'none';
            loginErrorDiv.innerText = '';

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    body: new FormData(loginForm)
                });
                
                if (response.ok) {
                    const result = await response.json();
                    if (result.success) {
                        window.location.reload(); // Sucesso, recarrega a página
                    }
                } else {
                    const errorResult = await response.json();
                    loginErrorDiv.innerText = errorResult.message || 'Erro inesperado.';
                    loginErrorDiv.style.display = 'block'; // Mostra o erro
                }
            } catch (error) {
                loginErrorDiv.innerText = 'Ocorreu um erro de comunicação.';
                loginErrorDiv.style.display = 'block';
            }
        });
    }

    // --- LÓGICA PARA O MODAL DE CADASTRO ---
    const registerForm = document.querySelector('#registerModal form');
    const registerErrorDiv = document.querySelector('#register-error-message');

    if (registerForm && registerErrorDiv) {
        registerForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            registerErrorDiv.style.display = 'none';
            registerErrorDiv.innerText = '';

            try {
                const response = await fetch('/users/add', {
                    method: 'POST',
                    body: new FormData(registerForm)
                });

                if (response.ok) {
                    const result = await response.json();
                    if (result.success) {
                        window.location.reload();
                    }
                } else {
                    const errorResult = await response.json();
                    registerErrorDiv.innerText = errorResult.message || 'Erro ao criar conta.';
                    registerErrorDiv.style.display = 'block';
                }
            } catch (error) {
                registerErrorDiv.innerText = 'Ocorreu um erro de comunicação. Tente novamente.';
                registerErrorDiv.style.display = 'block';
            }
        });
    }
});