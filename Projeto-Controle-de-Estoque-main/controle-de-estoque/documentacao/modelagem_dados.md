# Modelagem de Dados

[cite_start]A base de dados da aplicação, `inventory.db`, é composta por duas tabelas principais. 

### Tabela: `users`
Esta tabela armazena as credenciais e perfis dos usuários que podem acessar o sistema.

| Coluna | Tipo | Descrição | Restrições |
|---|---|---|---|
| `id` | INTEGER | Identificador único do usuário. | PRIMARY KEY, AUTOINCREMENT |
| `username` | TEXT | [cite_start]Nome de usuário para login. [cite: 49] | UNIQUE, NOT NULL |
| `password_hash` | TEXT | [cite_start]Senha criptografada com SHA-256. [cite: 53] | NOT NULL |
| `profile` | TEXT | [cite_start]Nível de acesso: 'Administrador' ou 'Comum'. [cite: 52, 66] | NOT NULL |

---

### Tabela: `products`
Esta tabela contém as informações de todos os produtos cadastrados no estoque.

| Coluna | Tipo | Descrição | Restrições |
|---|---|---|---|
| `id` | INTEGER | Identificador único do produto. | PRIMARY KEY, AUTOINCREMENT |
| `name` | TEXT | [cite_start]Nome do produto/material. [cite: 55] | NOT NULL |
| `description` | TEXT | Descrição detalhada do produto. | |
| `quantity` | INTEGER | Quantidade atual do produto em estoque. | NOT NULL |
| `min_quantity` | INTEGER | [cite_start]Quantidade mínima para gerar alerta visual.  | NOT NULL |