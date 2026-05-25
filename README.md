# Sistema Web SENAI Jaú

Sistema web desenvolvido em Python com Flask para gerenciamento e acesso a informações acadêmicas, cursos e autenticação de usuários.

---

# 📌 Sobre o Projeto

O Sistema Web SENAI Jaú foi criado com o objetivo de centralizar funcionalidades acadêmicas em uma aplicação simples, moderna e organizada.

A plataforma permite:

* Cadastro de usuários
* Login e autenticação
* Visualização de cursos
* Área de dashboard
* Navegação intuitiva
* Estrutura preparada para expansão futura

O projeto foi desenvolvido utilizando Python com Flask no backend e HTML/CSS no frontend.

---

# 🛠️ Tecnologias Utilizadas

## Backend

* Python 3
* Flask
* SQLite3

## Frontend

* HTML5
* CSS3
* JavaScript

## Ferramentas

* VS Code
* Git
* GitHub

---

# 📂 Estrutura do Projeto

```bash
senai-jau-system/
│
├── backend/
│   ├── app.py
│   ├── database.db
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── cursos.html
│   │   ├── dashboard.html
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Funcionalidades

## 👤 Sistema de Usuários

* Cadastro de contas
* Login seguro
* Sessão autenticada
* Logout

## 📚 Área de Cursos

* Visualização de cursos disponíveis
* Organização de conteúdo acadêmico
* Estrutura preparada para filtros e pesquisa

## 📊 Dashboard

* Painel principal do usuário
* Informações organizadas
* Navegação rápida

---

# 🚀 Como Executar o Projeto

## 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/senai-jau-system.git
```

---

## 2. Acesse a pasta do projeto

```bash
cd senai-jau-system
```

---

## 3. Crie um ambiente virtual

### Windows

```bash
python -m venv venv
```

### Linux/Mac

```bash
python3 -m venv venv
```

---

## 4. Ative o ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 5. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 6. Execute o sistema

```bash
python app.py
```

---

## 7. Acesse no navegador

```bash
http://127.0.0.1:5000
```

---

# 🗄️ Banco de Dados

O sistema utiliza SQLite para armazenamento local.

Arquivo principal:

```bash
database.db
```

O banco pode armazenar:

* Usuários
* Senhas criptografadas
* Cursos
* Informações acadêmicas

---

# 🔐 Segurança

O sistema possui:

* Validação de login
* Controle de sessão
* Estrutura para criptografia de senha
* Proteção básica contra acesso indevido

---

# 🎯 Objetivos do Projeto

Este projeto foi desenvolvido com foco em:

* Aprendizado de desenvolvimento web
* Integração backend/frontend
* Organização de aplicações Flask
* Boas práticas de programação
* Estruturação de sistemas escaláveis

---

# 📈 Melhorias Futuras

* Sistema de recuperação de senha
* Painel administrativo
* Integração com APIs
* Upload de arquivos
* Sistema de notas
* Responsividade avançada
* Banco de dados MySQL/PostgreSQL
* Deploy em nuvem

---

# 👨‍💻 Autor

Desenvolvido por Pedro Urchella.

Projeto acadêmico desenvolvido para estudos e práticas no SENAI.

---

# 📄 Licença

Este projeto possui finalidade educacional.

Uso livre para estudos e aprendizado.