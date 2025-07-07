# CineReviews: Seu Guia de Filmes e Avaliações

## Descrição da Solução e Funcionalidades

O **CineReviews** é uma aplicação web desenvolvida em Python utilizando o framework Bottle, projetada para gerenciar filmes, avaliações e listas personalizadas de usuários. 

### Funcionalidades Principais:

- Autenticação de Usuários: Sistema seguro de cadastro e login com hashing de senhas (bcrypt).

- Consulta de Filmes: Integração com a API do TMDb (The Movie Database) para buscar filmes populares ou pesquisar por títulos específicos.

- Páginas de Detalhes: Visualização completa de informações de um filme, incluindo sinopse, ano de lançamento, pôster e avaliações de outros usuários.

- Sistema de Avaliação: Usuários logados podem dar uma nota (de 1 a 5 estrelas) e deixar um comentário sobre os filmes.

- Lista de Favoritos: Funcionalidade para marcar filmes como favoritos.

- Perfil de Usuário: Página de perfil personalizada que exibe a lista de filmes favoritos e o histórico de avaliações do usuário.

### Requisitos para Pontuação Extra Adicionais:

Relações entre Models: (Cumprido)

- Um usuário pode ter várias avaliações (a classe Avaliacao armazena o id_usuario).

- Um usuário pode ter vários filmes favoritos, e um filme pode ser favoritado por vários usuários (a classe User possui uma lista de favorites com os IDs dos filmes).
  

Bibliotecas Adicionais:

- Além do Bottle, o projeto utiliza as bibliotecas bcrypt para segurança e requests para consumir a API do TMDb.
  

Qualidade do Projeto:

- O código está bem organizado, segue as boas práticas da estrutura MVC e inclui tratamento de erros, como nas chamadas de API.

## Estrutura do Projeto (MVC)

O projeto segue o padrão de arquitetura Model-View-Controller (MVC) para uma organização clara e modular do código. A estrutura de arquivos do seu projeto é a seguinte:


poo-python-bottle-template/
├── app.py
├── config.py
├── main.py
├── controllers/
├── models/
├── services/
├── views/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── data/
└── requirements.txt






---

## Descrição das Pastas

* **`app.py`**: Ponto de entrada principal da aplicação Bottle, onde as rotas são registradas e a aplicação é configurada.
* **`config.py`**: Contém configurações globais do projeto, como caminhos de arquivos de dados ou outras variáveis de ambiente.
* **`main.py`**: O script principal para iniciar o servidor web da aplicação.
* **`requirements.txt`**: Lista todas as bibliotecas Python das quais o projeto depende.
* **`controllers/`**: Contém as classes controladoras que lidam com a lógica de requisições HTTP, processam dados e interagem com os serviços e views.
    * `avaliacao_controller.py`: Gerencia rotas e lógica relacionadas a avaliações de filmes.
    * `base_controller.py`: Classe base para outros controladores, fornecendo métodos utilitários comuns (renderização de templates, gerenciamento de sessão, etc.).
    * `movie_controller.py`: Lida com rotas e funcionalidades de filmes (listagem, detalhes, adição/edição).
    * `user_controller.py`: Responsável pelas rotas e lógica de usuários (cadastro, login, perfil).
* **`models/`**: Define as classes que representam as entidades de dados do seu domínio (os "objetos" da sua aplicação).
    * `avaliacao.py`: Define a estrutura e o comportamento de uma avaliação de filme.
    * `movie.py`: Define a estrutura e o comportamento de um filme.
    * `user.py`: Define a estrutura e o comportamento de um usuário.
* **`services/`**: Contém a lógica de negócio e as operações de persistência de dados (leitura/escrita em arquivos JSON).
    * `api_service.py`: Responsável por interagir com APIs externas (se aplicável) para obter dados.
    * `avaliacao_service.py`: Gerencia a persistência e manipulação de dados de avaliações.
    * `movie_service.py`: Gerencia a persistência e manipulação de dados de filmes.
    * `user_service.py`: Gerencia a persistência e manipulação de dados de usuários.
* **`views/`**: Armazena os arquivos de template (`.tpl`) que o Bottle usa para renderizar as páginas HTML.
    * `avaliacao.tpl`: Template para exibir ou gerenciar avaliações.
    * `evaluate_movie_form.tpl`: Formulário para avaliar um filme.
    * `helper-final.tpl`: Um template auxiliar ou parte de layout.
    * `layout.tpl`: O template base que define a estrutura comum de todas as páginas (cabeçalho, rodapé, navegação).
    * `login_form.tpl`: Formulário de login de usuário.
    * `movies.tpl`: Lista de filmes.
    * `movies_form.tpl`: Formulário para adicionar/editar filmes.
    * `users.tpl`: Lista de usuários.
    * `user_form.tpl`: Formulário para cadastro/edição de usuário.
    * `user_profile.tpl`: Página de perfil do usuário.
* **`static/`**: Contém arquivos estáticos que são servidos diretamente pelo navegador.
    * `css/`: Folhas de estilo CSS (`helper.css`, `style.css`).
    * `img/`: Imagens usadas na aplicação (`imgprincipal.png`, `imoge.jpg`, `no_poster.png.png`).
    * `js/`: Arquivos JavaScript (`helper.js`, `main.js`).
* **`data/`**: Armazena os arquivos JSON que atuam como um banco de dados simples para persistir as informações da aplicação.
    * `movies.json`: Dados dos filmes.
    * `users.json`: Dados dos usuários.
    * `user_movie_lists.json`: Dados das listas de filmes personalizadas dos usuários.
* **`.vscode/`**: Contém configurações específicas para o ambiente de desenvolvimento VS Code.

---

## Modelagem de Dados e Pilares da OO

Nosso projeto utiliza as seguintes classes principais para modelagem de dados, com foco nos pilares da Orientação a Objetos:

* **`User` (models/user.py)**: Representa um usuário do sistema.
    * **Abstração**: Captura características essenciais como `id`, `name`, `email`, `birthdate`, `senha`.
    * **Encapsulamento**: Métodos como `set_password` encapsulam a lógica de hashing de senha.
* **`Movie` (models/movie.py)**: Representa um filme.
    * **Abstração**: Contém atributos como `id`, `name`, `ano`, `poster`, `resumo`, `avaliacao_media`, `comentarios`.
    * **Composição/Agregação**: Um `Movie` **agrega** uma lista de `Avaliacao` (comentários).
* **`Avaliacao` (models/avaliacao.py)**: Representa uma avaliação de um filme feita por um usuário.
    * **Abstração**: Atributos como `user_id`, `user_name`, `avaliacao`, `comentario_texto`, `timestamp`.

### Relações entre Models:

- Um usuário pode ter várias avaliações (a classe Avaliacao armazena o id_usuario).

- Um usuário pode ter vários filmes favoritos, e um filme pode ser favoritado por vários usuários (a classe User possui uma lista de favorites com os IDs dos filmes).

### Implementação dos 4 Pilares de OO:

* **Abstração**: Cada classe foca em representar um conceito específico do domínio, expondo apenas os detalhes relevantes.
* **Encapsulamento**: Atributos são acessados e modificados através de métodos, protegendo a integridade dos dados (ex: hashing de senha em `User`).
* **Herança**: A classe `BaseController` é herdada por todos os outros controladores, promovendo a reutilização de código para funcionalidades comuns como renderização de templates e gerenciamento de cookies de sessão.
* **Polimorfismo**: Embora não explicitamente demonstrado com interfaces complexas, o polimorfismo está presente na forma como diferentes modelos podem ser processados por métodos genéricos ou como diferentes controladores respondem a requisições HTTP de maneira única, mas com uma interface comum (ex: `setup_routes`).

---

## Instalação e Execução

Siga os passos abaixo para configurar e rodar a aplicação em seu ambiente local.

### Pré-requisitos:

* Python 3.8+
* `pip` (gerenciador de pacotes do Python)

### Passos:

1.  **Clone o Repositório:**
    ```bash
    git clone epf_OO_2025_main\epf_OO_2025-main
    cd epf_OO_2025_main\epf_OO_2025-main
    ```

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    # No Windows:
    .\venv\Scripts\activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    (Certifique-se de que o arquivo `requirements.txt` existe e lista `bottle`, `bcrypt`, `requests`, etc.)

4.  **Crie a Estrutura de Dados:**
    Certifique-se de que você tem a pasta `data/` na raiz do seu projeto. Dentro dela, crie os seguintes arquivos JSON vazios (com `[]`):
    * `data/users.json`
    * `data/movies.json`
    * `data/avaliacoes.json` (se você ainda estiver usando um arquivo separado para avaliações, caso contrário, as avaliações são salvas em `movies.json`)
    * `data/user_movie_lists.json`

    Certifique-se também de ter a pasta `static/img/` e, dentro dela, um arquivo `no_poster.png.png` (pode ser uma imagem placeholder simples).

5.  **Execute a Aplicação:**
    ```bash
    python main.py
    ```
    Você verá uma mensagem no terminal indicando que o servidor está rodando, geralmente em `http://localhost:8080/`.

6.  **Acesse a Aplicação:**
    Abra seu navegador e vá para `http://localhost:8080/`.

---

## Diagrama de Classes


![trabalho_OO drawio (3)](https://github.com/user-attachments/assets/23e210da-0c06-4e70-be3b-9e6615106809)


---

## Personalização

Para adicionar novas funcionalidades ou modelos ao projeto, siga a estrutura MVC existente:

1.  **Crie a classe no diretório `models/`**: Defina a estrutura de dados e o comportamento da nova entidade.
2.  **Crie o service correspondente em `services/`**: Implemente a lógica de persistência (leitura/escrita JSON) e manipulação de dados para o novo modelo.
3.  **Crie o controller em `controllers/`**: Defina as rotas e a lógica de interação com o usuário para a nova funcionalidade. Lembre-se de herdar de `BaseController`.
4.  **Crie as views `.tpl` associadas em `views/`**: Desenvolva as páginas HTML necessárias para a interface do usuário.
5.  **Atualize `app.py`**: Registre o novo controlador para que suas rotas sejam reconhecidas.
6.  **Atualize `requirements.txt`**: Se novas bibliotecas forem necessárias para a nova funcionalidade, adicione-as aqui.

---

## Tecnologias Utilizadas

* **Backend**: Python 3.x
* **Framework Web**: Bottle
* **Persistência de Dados**: JSON (arquivos locais)
* **Hashing de Senhas**: `bcrypt`
* **Requisições HTTP**: `requests` (para integração com APIs externas, se aplicável)
* **Frontend**: HTML5, CSS3
* **Framework CSS**: Bootstrap 5.3
* **Ícones**: Font Awesome
