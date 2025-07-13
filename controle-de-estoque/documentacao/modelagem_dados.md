# Modelagem de Dados

A base de dados da aplicação, `inventory.db`, é composta por duas tabelas principais. 

### Tabela: `users`
Esta tabela armazena as credenciais e perfis dos usuários que podem acessar o sistema.

| Coluna | Tipo | Descrição | Restrições |
|---|---|---|---|
| `id` | INTEGER | Identificador único do usuário. | PRIMARY KEY, AUTOINCREMENT |
| `username` | TEXT | Nome de usuário para login.  | UNIQUE, NOT NULL |
| `password_hash` | TEXT | Senha criptografada com SHA-256.  | NOT NULL |
| `profile` | TEXT | Nível de acesso: 'Administrador' ou 'Comum'. | NOT NULL |

---

### Tabela: `products`
Esta tabela contém as informações de todos os produtos cadastrados no estoque.

| Coluna | Tipo | Descrição | Restrições |
|---|---|---|---|
| `id` | INTEGER | Identificador único do produto. | PRIMARY KEY, AUTOINCREMENT |
| `name` | TEXT | Nome do produto/material.  | NOT NULL |
| `description` | TEXT | Descrição detalhada do produto. | |
| `quantity` | INTEGER | Quantidade atual do produto em estoque. | NOT NULL |
| `min_quantity` | INTEGER | Quantidade mínima para gerar alerta visual.  | NOT NULL |