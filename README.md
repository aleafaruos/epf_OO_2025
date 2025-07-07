# Projeto Template: POO com Python + Bottle + JSON

Este é um projeto de template educacional voltado para o ensino de **Programação Orientada a Objetos (POO)** do Prof. Lucas Boaventura, Universidade de Brasília (UnB).

Utiliza o microframework **Bottle**. Ideal para uso em disciplinas introdutórias de Engenharia de Software ou Ciência da Computação.

## 💡 Objetivo

Fornecer uma base simples, extensível e didática para construção de aplicações web orientadas a objetos com aplicações WEB em Python, ideal para trabalhos finais ou exercícios práticos.

---

## 🗂 Estrutura de Pastas

```bash
CineReviews/
├── .vscode/
│   └── settings.json
├── controllers/
│   ├── avaliacao_controller.py
│   ├── base_controller.py
│   ├── movie_controller.py
│   ├── user_controller.py
│   └── init.py
├── data/
│   ├── movies.json
│   ├── users.json
│   └── user_movie_lists.json
├── models/
│   ├── avaliacao.py
│   ├── movie.py
│   ├── user.py
│   └── init.py
├── services/
│   ├── api_service.py
│   ├── avaliacao_service.py
│   ├── movie_service.py
│   ├── user_service.py
│   └── init.py
├── static/
│   ├── css/
│   │   ├── helper.css
│   │   └── style.css
│   ├── img/
│   │   ├── imgprincipal.png
│   │   ├── imoge.jpg
│   │   └── no_poster.png.png
│   └── js/
│       ├── helper.js
│       └── main.js
├── views/
│   ├── avaliacao.tpl
│   ├── evaluate_movie_form.tpl
│   ├── helper-final.tpl
│   ├── layout.tpl
│   ├── login_form.tpl
│   ├── movies.tpl
│   ├── movies_form.tpl
│   ├── users.tpl
│   ├── user_form.tpl
│   └── user_profile.tpl
├── .gitignore
├── .pylintrc
├── app.py
├── config.py
├── main.py
├── Makefile
├── migrate_json.py
├── README.md
└── requirements.txt
```


---

## 📁 Descrição das Pastas

Nosso projeto utiliza as seguintes classes principais para modelagem de dados, com foco nos pilares da Orientação a Objetos:

* **`User` (models/user.py)**: Representa um usuário do sistema.
    * **Abstração**: Captura características essenciais como `id`, `name`, `email`, `birthdate`, `senha`.
    * **Encapsulamento**: Métodos como `set_password` encapsulam a lógica de hashing de senha.
* **`Movie` (models/movie.py)**: Representa um filme.
    * **Abstração**: Contém atributos como `id`, `name`, `ano`, `poster`, `resumo`, `avaliacao_media`, `comentarios`.
    * **Composição/Agregação**: Um `Movie` **agrega** uma lista de `Avaliacao` (comentários).
* **`Avaliacao` (models/avaliacao.py)**: Representa uma avaliação de um filme feita por um usuário.
    * **Abstração**: Atributos como `user_id`, `user_name`, `avaliacao`, `comentario_texto`, `timestamp`.

### Implementação dos 4 Pilares de OO:

* **Abstração**: Cada classe foca em representar um conceito específico do domínio, expondo apenas os detalhes relevantes.
* **Encapsulamento**: Atributos são acessados e modificados através de métodos, protegendo a integridade dos dados (ex: hashing de senha em `User`).
* **Herança**: A classe `BaseController` é herdada por todos os outros controladores, promovendo a reutilização de código para funcionalidades comuns como renderização de templates e gerenciamento de cookies de sessão.
* **Polimorfismo**: Embora não explicitamente demonstrado com interfaces complexas, o polimorfismo está presente na forma como diferentes modelos podem ser processados por métodos genéricos ou como diferentes controladores respondem a requisições HTTP de maneira única, mas com uma interface comum (ex: `setup_routes`).

---

## ▶️ Como Executar

### Pré-requisitos:

* Python 3.8+
* `pip` 

### Passos:

1.  **Clone o Repositório:**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd [pasta_do_seu_repositorio]
    ```

2.  **Crie e Ative um Ambiente Virtual:**
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

4.  **Crie a Estrutura de Dados:**
    Certifique-se de que você tem a pasta `data/` na raiz do seu projeto. Dentro dela, crie os seguintes arquivos JSON vazios (com `[]`):
    * `data/users.json`
    * `data/movies.json`
    * `data/user_movie_lists.json`

    Certifique-se também de ter a pasta `static/images/` e, dentro dela, um arquivo `no_poster.png.png`.

5.  **Execute a Aplicação:**
    ```bash
    python main.py
    ```
    Você verá uma mensagem no terminal indicando que o servidor está rodando, geralmente em `http://localhost:8080/`.

6.  **Acesse a Aplicação:**
    Abra seu navegador e vá para `http://localhost:8080/`.

---

![trabalho_OO drawio (3)](https://github.com/user-attachments/assets/bfe6aadf-5510-4632-a39a-0f09f26014b6)

---

## ✍️ Personalização
Para adicionar novos modelos (ex: Atividades):

1. Crie a classe no diretório **models/**.

2. Crie o service correspondente para manipulação do JSON.

3. Crie o controller com as rotas.

4. Crie as views .tpl associadas.

---
## Autores 

* Flávia Rebelato - 
* Rafaela Santos Cerqueira - 242015700
---

## 🧠 Autor e Licença
Projeto desenvolvido como template didático para disciplinas de Programação Orientada a Objetos, baseado no [BMVC](https://github.com/hgmachine/bmvc_start_from_this).
Você pode reutilizar, modificar e compartilhar livremente.
