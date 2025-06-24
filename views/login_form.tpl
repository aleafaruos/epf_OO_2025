% rebase('layout', title='Login')

<section class="form-section">
    <h1>Login de Usuário</h1>

    % if defined('error_message') and error_message:
    <p class="error-message">{{error_message}}</p>
    % end

    <form action="/login" method="post" class="form-container">
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required value="{{email or ''}}">
        </div>

        <div class="form-group">
            <label for="senha">Senha:</label>
            <input type="password" id="senha" name="senha" required>
        </div>

        <div class="form-actions">
            <button type="submit" class="btn-submit">Entrar</button>
            <a href="/users/add" class="btn-cancel">Criar Conta</a> </div>
    </form>
</section>

<style>
    .error-message {
        color: red;
        background-color: #ffe0e0;
        border: 1px solid red;
        padding: 10px;
        margin-bottom: 20px;
        border-radius: 5px;
        text-align: center;
    }
</style>