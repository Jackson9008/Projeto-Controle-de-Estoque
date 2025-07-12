# Fluxograma da Aplicação

[cite_start]Este documento descreve o fluxo lógico da aplicação de controle de estoque, desde o início até as principais interações do usuário. [cite: 42]

1.  **Início**
    * O usuário executa o arquivo `app.py`.

2.  [cite_start]**Tela de Login [cite: 49]**
    * A aplicação exibe a tela de login solicitando "Usuário" e "Senha".
    * O usuário preenche os campos e clica em "Entrar".
    * **Processo de Validação:**
        * O sistema criptografa a senha digitada.
        * Consulta a tabela `users` no banco de dados, buscando um `username` correspondente.
        * Se o usuário existe, compara a senha criptografada com a `password_hash` armazenada.
    * **Resultado da Validação:**
        * **Falha:** Uma mensagem de "Usuário ou senha inválidos" é exibida. O usuário permanece na tela de login.
        * **Sucesso:** O sistema armazena as informações do usuário (nome, perfil) e avança para a Tela Principal.

3.  **Tela Principal**
    * A tela exibe uma mensagem de boas-vindas com o nome e o perfil do usuário logado.
    * [cite_start]**Listagem de Produtos:** Uma tabela exibe todos os produtos cadastrados. 
        * **Alerta Visual:** Se `quantity` <= `min_quantity`, a linha do produto é destacada com a cor vermelha.
    * **Funcionalidades de Produto:** Botões para "Adicionar", "Atualizar" e "Excluir" produtos estão disponíveis para todos os usuários.
    * **Funcionalidade de Usuário:**
        * [cite_start]**Verificação de Perfil:** O sistema verifica se o perfil do usuário é 'Administrador'. 
        * [cite_start]Se **Administrador**: O botão "Cadastrar Novo Usuário" fica visível e funcional. 
        * Se **Comum**: O botão é ocultado ou desabilitado.

4.  **Ações e Janelas Secundárias**
    * **Adicionar/Editar Produto:** Ao clicar nos botões, os campos do formulário são usados para inserir ou atualizar dados. [cite_start]Validações garantem que campos numéricos recebam números e que campos obrigatórios sejam preenchidos. [cite: 44, 56]
    * **Cadastrar Novo Usuário (Admin):** Clicar no botão abre uma nova janela para cadastro, solicitando nome, senha e perfil ('Comum' ou 'Administrador').

5.  **Logout**
    * O usuário clica em "Sair".
    * A sessão atual é encerrada, e o sistema retorna para a Tela de Login.