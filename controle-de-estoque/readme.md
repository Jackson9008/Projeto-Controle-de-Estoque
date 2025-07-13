# Projeto: Sistema de Controle de Estoque em Python

Este é um projeto acadêmico desenvolvido para a matéria de "Case Development with Python" da UniFECAF, que consiste em uma aplicação desktop para gerenciamento de estoque.

## 🎯 Objetivo

O objetivo é criar uma aplicação funcional e segura para controlar a entrada e saída de produtos, com diferentes níveis de acesso para usuários, atendendo aos requisitos propostos no estudo de caso. 

## ✨ Funcionalidades Principais

**Autenticação de Usuário:** Tela de login segura para acesso ao sistema. 
**Segurança:** Senhas criptografadas usando o algoritmo SHA-256. 
    **Perfis de Usuário:**
    **Administrador:** Acesso total, incluindo o cadastro de novos usuários. 
    **Comum:** Acesso às funcionalidades de gerenciamento de produtos, mas sem permissão para cadastrar usuários. 
* **Gerenciamento de Produtos (CRUD):**
    * **C**reate: Adicionar novos produtos ao estoque.
    * **R**ead: Visualizar todos os produtos em uma lista clara e organizada.
    * **U**pdate: Editar as informações de produtos existentes.
    * **D**elete: Remover produtos do estoque.
**Alertas Visuais:** Produtos com quantidade em estoque abaixo do mínimo definido são destacados em vermelho para fácil identificação. 
**Interface Intuitiva:** Uma interface gráfica simples e fácil de usar, desenvolvida com Tkinter. 

## 🛠️ Tecnologias Utilizadas

**Linguagem:** Python 3 
**Interface Gráfica:** Tkinter 
**Banco de Dados:** SQLite3 
**Criptografia:** hashlib 

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

## Como testar aplicação: 
**Cenário de Teste 1: Autenticação, Segurança e Sessão de Usuário.**

**Passos a Executar**
1.1

Na tela de login, deixe os campos "Usuário" e "Senha" vazios e clique em "Entrar".
Uma janela de erro deve aparecer com a mensagem "Usuário e senha não podem ser vazios.". 
Validações nos campos , 


**Validação e autenticação do usuário**
1.2

Digite um usuário inválido (ex: teste) e qualquer senha. Clique em "Entrar".
Uma janela de erro deve aparecer com a mensagem "Usuário ou senha inválidos.".

**Validação e autenticação do usuário** 
1.3

Digite o usuário admin e uma senha incorreta (ex: 12345). Clique em "Entrar".
Uma janela de erro deve aparecer com a mensagem "Usuário ou senha inválidos.".
Criptografia de senha (A comparação é feita com o hash, não com texto plano), 

**Validação do usuário** 
1.4

Digite o usuário admin e a senha correta admin. Clique em "Entrar".
A tela de login fecha e a tela principal da aplicação é exibida. A mensagem "Bem-vindo(a), admin (Administrador)" deve aparecer.

Validação de usuário (login e senha) , 
Conexão com o banco de dados , 
Sessão de usuário , 

**Perfil de usuário** 

1.5
Na tela principal, clique no botão "Sair".
A tela principal fecha e a aplicação retorna para a tela de login.
Sessão de usuário , 
Facilidade de navegação.


## Cenário de Teste 2: Gerenciamento de Produtos (CRUD) ##

2.1

**(Validação)** Na tela principal, com os campos de produto vazios, clique em "Adicionar Produto".

Uma janela de erro deve aparecer com a mensagem "Nome, Quantidade e Qtd. Mínima são campos obrigatórios.". 


Validações nos campos , 

Conter campo obrigatório 

2.2

**(Validação)** Preencha o nome, mas coloque um texto no campo "Quantidade" (ex: abc). Clique em "Adicionar Produto".

Uma janela de erro deve aparecer com a mensagem "Quantidade e Qtd. Mínima devem ser números inteiros.". 


Validações nos campos 

2.3

**(Adicionar)** Preencha os campos com dados válidos (ex: Nome: Mouse sem fio, Descrição: Logitech MX, Qtd: 20, Qtd. Mínima: 10). Clique em "Adicionar Produto".

Uma mensagem de sucesso aparece e o novo produto é exibido na lista. Os campos do formulário são limpos.


Cadastro de produto / material no estoque 

2.4

**(Alerta Visual)** Adicione outro produto onde a quantidade é menor que a mínima (ex: Nome: Teclado Gamer, Qtd: 4, Qtd. Mínima: 5).

O produto Teclado Gamer deve aparecer na lista com a linha destacada em cor diferente (vermelho/salmão).


Listagem de produtos abaixo de uma quantidade mínima colocar em destaque 

2.5

**(Editar)** Selecione o Mouse sem fio na lista. Os dados devem preencher o formulário. Altere a quantidade para 15 e clique em "Atualizar Produto".

Uma mensagem de sucesso aparece e a quantidade do mouse na lista é atualizada para 15.


realizando edição para atualizar a entrada e/ou saída de mercadorias 

2.6

**(Excluir)** Selecione o Mouse sem fio na lista. Clique em "Excluir Produto". Uma janela de confirmação deve aparecer. Clique em "Sim".

O produto Mouse sem fio desaparece da lista.


## Cenário de Teste 3: Controle de Acesso por Perfil de Usuário ##

Passos a Executar

3.1

**(Admin)** Logado como admin, verifique a seção "Gerenciamento de Usuários".

O botão "Cadastrar Novo Usuário" deve estar visível e habilitado.


Somente o usuário administrador pode cadastrar , 


Mínimo 2 tipos de perfis (Administrador / Comum) 

3.2

**(Admin)** Clique em "Cadastrar Novo Usuário". Na nova janela, cadastre um usuário com os dados: Usuário: joao, Senha: 123, Perfil: Comum. Clique em "Cadastrar".

Uma mensagem de sucesso aparece e a janela de cadastro fecha.


Somente administrador poderá cadastrar usuário 


3.3

**(Logout e Login Comum)** Clique em "Sair" para fazer logout. Faça login com o novo usuário: joao e senha 123.

O login é bem-sucedido. A tela principal exibe a mensagem "Bem-vindo(a), joao (Comum)".


Login e senha para validar o usuário 

3.4

**(Verificação de Permissão)** Logado como joao (Comum), verifique a seção "Gerenciamento de Usuários".

O botão "Cadastrar Novo Usuário" NÃO deve estar visível. Em seu lugar, deve haver um texto informativo (ex: "Apenas administradores podem cadastrar...").


Perfil de usuário (Administrador / Comum) , 

Somente o usuário administrador pode cadastrar 


3.5

**(Funcionalidade Comum)** Logado como joao, tente adicionar, editar e excluir um produto.

Todas as operações de gerenciamento de produtos (Cenário 2) devem funcionar normalmente para o usuário comum.


desenvolver uma aplicação de controle de estoque, onde será possível cadastrar um produto realizando edição...

