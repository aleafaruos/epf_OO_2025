<!DOCTYPE html>
<html lang="pt-br">
<head>
    <title>Sistema Filmes - {{title or 'Sistema'}}</title>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/css/style.css" />
</head>
<body link="black" alink="black" vlink="black">
    <center>
    <font face="Bold" size="3">
        <a href="">FILMES</a>
        <a href="">CRÍTICA</a>
        <a href="">LOGIN</a>
        <a href="">PERFIL</a>
        <a href="">AVALIAÇÕES</a>
    </font>
    </center>

    <img src="/static/img/imoge.jpg" alt="imagem filme interestelar" width="100%" height="">
    <h1>Filmes UnB</h1>
    <center>
    <font face="Georgia" size="5" color=>
        <p><strong>Acompanhe os filmes que você assistiu.</strong></p>
        <p><strong>Salve aqueles que você quer ver.</strong></p>
        <p><strong>Compartilhe com seus amigos o que é bom.</strong></p>
    </font>
    </center>

    <center>
    <p> CRIE SUA CONTA!</p>
    </center>
    <br>
    <p>Nos acompanhe por <img src="" alt=""></p>
    <hr/>

    <table border="1">
        <tr>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td> 
        </tr>
    </table>


    <br>
    <p>ENCONTRE NO UNB FILMES...</p> 
    <table border="1">
    
        <tr>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
        </tr>
         <tr>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
        </tr>
    </table>

    <br>
    <hr/>
    <p>FILMES AVALIADOS</p>

    <table border="1">
        <tr>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>
            <td>imagem</td>  
        </tr>
    </table>
    <center>
        <h3>Escreva e compartilhe resenhas. Crie suas próprias listas. Compartilhe sua vida no cinema.</h2>
            <h4>Abaixo estão algumas análises e listas populares desta semana. <a href="">Cadastre-se</a> para criar a sua.</h4>
    </center>
    
    <br>
    <p>Avaliações populares desta semana</p>
    <hr/>
    <br>

    <table border="1">
        <tr>
            <td><img src=""/></td>
            <td>texto</td>
        </tr>
        <tr>
            <td><img src=""/></td>
            <td>texto</td>
        </tr>
        <tr>
            <td><img src="/static/img/imoge.jpg" width="200"/></td>
            <td>texto</td>
        </tr>
        <tr>
            <td><img src=""/></td>
            <td>texto</td>
        </tr>
        <tr>
            <td><img src=""/></td>
            <td>texto</td>
        </tr>
        <tr>
            <td><img src=""/></td>
            <td>texto</td>
        </tr>
    </table>

    <div class="container">
        {{!base}}  <!-- O conteúdo das páginas filhas virá aqui -->
    </div>

    <footer>
        <p>&copy; 2025, Meu Projetinho. Todos os direitos reservados.</p>
    </footer>

    <!-- Scripts JS no final do body -->
    <script src="/static/js/main.js"></script>
</body>
</html>
