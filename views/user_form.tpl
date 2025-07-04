%rebase('layout', title='Cadastro de Usuário')

<h1>{{'Editar Usuário' if user else 'Novo Usuário'}}</h1>

% if error_message:
    <p style="color: red;">{{error_message}}</p>
% end

<form action="{{action}}" method="post">
    <label for="name">Nome:</label><br>
    <input type="text" name="name" value="{{user.name if user else ''}}" required><br><br>

    <label for="email">Email:</label><br>
    <input type="email" name="email" value="{{user.email if user else ''}}" required><br><br>

    <label for="birthdate">Data de Nascimento:</label><br>
    <input type="date" name="birthdate" value="{{user.birthdate if user else ''}}" required><br><br>

    <label for="senha">Senha:</label><br>
    <input type="password" name="senha" required><br><br>

    <button type="submit">{{'Salvar Alterações' if user else 'Cadastrar'}}</button>
</form>

<p><a href="/users">Voltar</a></p>
