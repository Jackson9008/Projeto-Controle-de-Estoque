# Projeto: Sistema de Controle de Estoque em Python

Este é um projeto acadêmico desenvolvido para a matéria de "Case Development with Python" da UniFECAF, que consiste em uma aplicação desktop para gerenciamento de estoque. 

## 🎯 Objetivo

O objetivo é criar uma aplicação funcional e segura para controlar a entrada e saída de produtos, com diferentes níveis de acesso para usuários, atendendo aos requisitos propostos no estudo de caso.

## ✨ Funcionalidades Principais

* **Autenticação de Usuário:** Tela de login segura para acesso ao sistema. 
* **Segurança:**Senhas criptografadas usando o algoritmo SHA-256. 
* **Perfis de Usuário:**
    * **Administrador:** Acesso total, incluindo o cadastro de novos usuários. 
    * **Comum:** Acesso às funcionalidades de gerenciamento de produtos, mas sem permissão para cadastrar usuários. 
* **Gerenciamento de Produtos (CRUD):**
    * **Create:** Adicionar novos produtos ao estoque.
    * **Read:** Visualizar todos os produtos em uma lista clara e organizada.
    * **Update:** Editar as informações de produtos existentes.
    * **Delete:** Remover produtos do estoque.
* **Alertas Visuais:** Produtos com quantidade em estoque abaixo do mínimo definido são destacados em vermelho para fácil identificação. 
* **Interface Intuitiva:** Uma interface gráfica simples e fácil de usar, desenvolvida com Tkinter.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3 
* **Interface Gráfica:** Tkinter 
* **Banco de Dados:** SQLite3 
* **Criptografia:** hashlib

## 🚀 Como Executar o Projeto

1.  **Pré-requisitos:**
    * Ter o Python 3 instalado em seu computador.

2.  **Clonar o Repositório (se estiver no Git):**
    ```bash
    git clone <url-do-seu-repositorio>
    cd controle-de-estoque
    ```

3.  **Configurar o Banco de Dados:**
    Execute o script `database.py` **uma única vez** para criar o arquivo `inventory.db` e o usuário administrador padrão.
    ```bash
    python database.py
    ```
    * Isso criará o usuário: `admin` com a senha: `admin`.

4.  **Executar a Aplicação:**
    Agora, rode o arquivo principal da aplicação.
    ```bash
    python app.py
    ```

5.  **Acessar o Sistema:**
    * Use as credenciais `admin` / `admin` para entrar como administrador.
    * Como administrador, você pode cadastrar novos usuários (comuns ou outros administradores) através do botão "Cadastrar Novo Usuário".

## 📂 Estrutura do Projeto

/controle-de-estoque
|
|-- readme.md                # Esta documentação
|-- database.py              # Script de setup do banco de dados
|-- app.py                   # Código fonte principal da aplicação
|-- inventory.db             # Arquivo do banco de dados (gerado após a execução de database.py)
|
+-- /documentacao
|
|-- modelagem_dados.md   # Detalhes da modelagem do banco de dados
|-- fluxograma.md        # Descrição do fluxo da aplicação
