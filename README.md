Sistema de Estoque com Flask
Este é um sistema de gerenciamento de estoque desenvolvido em Python utilizando o framework Flask. O sistema permite o cadastro de produtos, controle de estoque, alertas de estoque baixo e gerenciamento de usuários com dois perfis: administrador e comum.

Funcionalidades
Autenticação de Usuários:

Login e senha.

Dois perfis: administrador e comum.

Cadastro de Produtos:

Campos obrigatórios: nome, quantidade e quantidade mínima.

Apenas usuários administradores podem cadastrar produtos.

Listagem de Produtos:

Exibe todos os produtos cadastrados.

Destaque para produtos com quantidade abaixo do mínimo.

Cadastro de Usuários:

Apenas usuários administradores podem cadastrar novos usuários.

Segurança:

Criptografia de senhas (usando bcrypt).

Sessão de usuário para controle de acesso.

Tecnologias Utilizadas
Python: Linguagem de programação principal.

Flask: Framework web para desenvolvimento do back-end.

SQLite: Banco de dados para armazenamento de informações.

Bcrypt: Biblioteca para criptografia de senhas.

HTML/CSS: Para a interface do usuário.

Pré-requisitos
Antes de começar, certifique-se de ter instalado:

Python 3.x

Pip (gerenciador de pacotes do Python)

Como Executar o Projeto
Clone o repositório:

bash
Copy
git clone https://github.com/seu-usuario/sistema-estoque-flask.git
cd sistema-estoque-flask
Crie um ambiente virtual (opcional, mas recomendado):

bash
Copy
python -m venv venv
Ative o ambiente virtual:

No Windows:

bash
Copy
.\venv\Scripts\activate
No macOS/Linux:

bash
Copy
source venv/bin/activate
Instale as dependências:

bash
Copy
pip install -r requirements.txt
Execute o aplicativo:

bash
Copy
python app.py
Acesse o sistema:

Abra o navegador e acesse:

Copy
http://127.0.0.1:5000
Estrutura do Projeto
Copy
sistema-estoque-flask/
├── app.py                  # Código principal do Flask
├── requirements.txt        # Lista de dependências
├── sistema_estoque.db      # Banco de dados SQLite
├── templates/              # Templates HTML
│   ├── login.html          # Página de login
│   ├── menu.html           # Menu principal
│   ├── cadastro_produto.html # Página de cadastro de produtos
│   ├── listar_produtos.html  # Página de listagem de produtos
│   ├── cadastro_usuario.html # Página de cadastro de usuários
├── static/                 # Arquivos estáticos (CSS, JS, etc.)
│   └── styles.css          # Estilos CSS
Banco de Dados
O banco de dados utilizado é o SQLite. As tabelas são criadas automaticamente ao executar o aplicativo pela primeira vez. Aqui está o esquema do banco de dados:

Tabela usuarios
Coluna	Tipo	Descrição
id	INTEGER	Chave primária, autoincrementada.
nome	TEXT	Nome do usuário.
login	TEXT	Login único do usuário.
senha	TEXT	Senha criptografada.
perfil	TEXT	Perfil do usuário (admin/comum).
Tabela produtos
Coluna	Tipo	Descrição
id	INTEGER	Chave primária, autoincrementada.
nome	TEXT	Nome do produto.
quantidade	INTEGER	Quantidade em estoque.
quantidade_minima	INTEGER	Quantidade mínima necessária.
