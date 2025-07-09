# controle-de-estoque/app.py

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib

# --- Funções de Utilitário ---

def hash_password(password):
    """Criptografa a senha usando SHA-256."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def connect_db():
    """Conecta ao banco de dados SQLite."""
    return sqlite3.connect('inventory.db')

# --- Classes da Aplicação ---

class StockControlApp(tk.Tk):
    """Classe principal da aplicação que gerencia as janelas."""
    def __init__(self):
        super().__init__()
        self.title("Sistema de Controle de Estoque")
        self.geometry("800x600")

        self.current_user = None
        
        # Container principal
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        """Mostra uma janela (frame) específica."""
        # Destroi o frame antigo para limpar a tela
        for widget in self.container.winfo_children():
            widget.destroy()

        # Cria a nova instância do frame
        if page_name == "LoginFrame":
            frame = LoginFrame(parent=self.container, controller=self)
        elif page_name == "MainFrame":
            frame = MainFrame(parent=self.container, controller=self)
        else:
            raise ValueError(f"Frame {page_name} não encontrado.")
            
        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def login_success(self, user_info):
        """Callback chamado após o login bem-sucedido."""
        self.current_user = user_info
        self.show_frame("MainFrame")

    def logout(self):
        """Realiza o logout e retorna à tela de login."""
        self.current_user = None
        self.show_frame("LoginFrame")


class LoginFrame(tk.Frame):
    """Frame da tela de login."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Login do Sistema", font=("Arial", 16)).pack(pady=20)

        tk.Label(self, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)
        self.username_entry.focus()

        tk.Label(self, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Entrar", command=self.check_login)
        login_button.pack(pady=20)
        
        self.bind_all("<Return>", lambda event: self.check_login())

    def check_login(self):
        """Valida as credenciais do usuário no banco de dados."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Erro de Login", "Usuário e senha não podem ser vazios.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, username, password_hash, profile FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user[2] == hash_password(password):
            user_info = {'id': user[0], 'username': user[1], 'profile': user[3]}
            self.controller.login_success(user_info)
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")


class MainFrame(tk.Frame):
    """Frame principal da aplicação após o login."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # --- Layout ---
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", pady=10, padx=10)

        user_info = self.controller.current_user
        welcome_text = f"Bem-vindo(a), {user_info['username']} ({user_info['profile']})"
        tk.Label(top_frame, text=welcome_text, font=("Arial", 12)).pack(side="left")

        logout_button = tk.Button(top_frame, text="Sair", command=self.controller.logout)
        logout_button.pack(side="right")
        
        # Separador visual
        ttk.Separator(self, orient='horizontal').pack(fill='x', padx=10, pady=5)
        
        # Frame de gerenciamento
        management_frame = tk.Frame(self)
        management_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.create_product_widgets(management_frame)
        self.create_user_widgets(management_frame)
        self.load_products()

    def create_product_widgets(self, parent_frame):
        """Cria os widgets para gerenciamento de produtos."""
        product_frame = ttk.LabelFrame(parent_frame, text="Gerenciamento de Produtos")
        product_frame.pack(fill="both", expand=True, pady=10)

        # Formulário de produto
        form_frame = tk.Frame(product_frame)
        form_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky="w", padx=5)
        self.name_entry = tk.Entry(form_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky="ew")

        tk.Label(form_frame, text="Descrição:").grid(row=1, column=0, sticky="w", padx=5)
        self.desc_entry = tk.Entry(form_frame, width=40)
        self.desc_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(form_frame, text="Quantidade:").grid(row=0, column=2, sticky="w", padx=5)
        self.qty_entry = tk.Entry(form_frame, width=10)
        self.qty_entry.grid(row=0, column=3)

        tk.Label(form_frame, text="Qtd. Mínima:").grid(row=1, column=2, sticky="w", padx=5)
        self.min_qty_entry = tk.Entry(form_frame, width=10)
        self.min_qty_entry.grid(row=1, column=3)

        form_frame.grid_columnconfigure(1, weight=1)

        # Botões de Ação
        button_frame = tk.Frame(product_frame)
        button_frame.pack(fill="x", pady=10)

        tk.Button(button_frame, text="Adicionar Produto", command=self.add_product).pack(side="left", padx=5)
        tk.Button(button_frame, text="Atualizar Produto", command=self.update_product).pack(side="left", padx=5)
        tk.Button(button_frame, text="Excluir Produto", command=self.delete_product).pack(side="left", padx=5)
        tk.Button(button_frame, text="Limpar Campos", command=self.clear_fields).pack(side="left", padx=5)

        # Tabela de produtos
        columns = ('id', 'name', 'description', 'quantity', 'min_quantity')
        self.tree = ttk.Treeview(product_frame, columns=columns, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='Nome')
        self.tree.heading('description', text='Descrição')
        self.tree.heading('quantity', text='Quantidade')
        self.tree.heading('min_quantity', text='Qtd. Mínima')

        self.tree.column('id', width=50, anchor='center')
        self.tree.column('name', width=200)
        self.tree.column('description', width=250)
        self.tree.column('quantity', width=80, anchor='center')
        self.tree.column('min_quantity', width=80, anchor='center')

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        
        # Configuração da tag para estoque baixo
        self.tree.tag_configure('low_stock', background='salmon')

    def create_user_widgets(self, parent_frame):
        """Cria os widgets para gerenciamento de usuários (visível apenas para admin)."""
        user_frame = ttk.LabelFrame(parent_frame, text="Gerenciamento de Usuários")
        user_frame.pack(fill="x", pady=10)
        
        user_info = self.controller.current_user
        if user_info['profile'] == 'Administrador':
            self.add_user_button = tk.Button(user_frame, text="Cadastrar Novo Usuário", command=self.open_user_registration)
            self.add_user_button.pack(pady=10, padx=10)
        else:
            tk.Label(user_frame, text="Apenas administradores podem cadastrar novos usuários.").pack(pady=10, padx=10)

    # --- Funções CRUD de Produtos ---
    
    def validate_fields(self):
        """Valida se os campos de produto foram preenchidos corretamente."""
        name = self.name_entry.get()
        qty_str = self.qty_entry.get()
        min_qty_str = self.min_qty_entry.get()

        if not name or not qty_str or not min_qty_str:
            messagebox.showerror("Erro de Validação", "Nome, Quantidade e Qtd. Mínima são campos obrigatórios.")
            return False

        try:
            int(qty_str)
            int(min_qty_str)
        except ValueError:
            messagebox.showerror("Erro de Validação", "Quantidade e Qtd. Mínima devem ser números inteiros.")
            return False
        
        return True

    def add_product(self):
        """Adiciona um novo produto ao banco de dados."""
        if not self.validate_fields():
            return
            
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, description, quantity, min_quantity) VALUES (?, ?, ?, ?)",
            (self.name_entry.get(), self.desc_entry.get(), int(self.qty_entry.get()), int(self.min_qty_entry.get()))
        )
        conn.commit()
        conn.close()
        
        self.load_products()
        self.clear_fields()
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")

    def update_product(self):
        """Atualiza um produto selecionado."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Nenhum produto selecionado para atualizar.")
            return
        
        if not self.validate_fields():
            return

        product_id = self.tree.item(selected_item)['values'][0]
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE products SET name=?, description=?, quantity=?, min_quantity=? WHERE id=?",
            (self.name_entry.get(), self.desc_entry.get(), int(self.qty_entry.get()), int(self.min_qty_entry.get()), product_id)
        )
        conn.commit()
        conn.close()
        
        self.load_products()
        self.clear_fields()
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        
    def delete_product(self):
        """Exclui um produto selecionado."""
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror("Erro", "Nenhum produto selecionado para excluir.")
            return

        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir o produto selecionado?"):
            product_id = self.tree.item(selected_item)['values'][0]
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            conn.close()
            
            self.load_products()
            self.clear_fields()
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

    def load_products(self):
        """Carrega e exibe todos os produtos do banco de dados na Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, quantity, min_quantity FROM products ORDER BY name")
        
        for row in cursor.fetchall():
            quantity = row[3]
            min_quantity = row[4]
            # Aplica a tag 'low_stock' se a quantidade for menor ou igual à mínima
            tags = ('low_stock',) if quantity <= min_quantity else ()
            self.tree.insert('', 'end', values=row, tags=tags)
            
        conn.close()

    def clear_fields(self):
        """Limpa os campos do formulário de produto."""
        self.name_entry.delete(0, 'end')
        self.desc_entry.delete(0, 'end')
        self.qty_entry.delete(0, 'end')
        self.min_qty_entry.delete(0, 'end')
        self.tree.selection_remove(self.tree.selection()) # Desseleciona item na tabela

    def on_item_select(self, event):
        """Preenche o formulário quando um item da tabela é selecionado."""
        selected_item = self.tree.focus()
        if not selected_item:
            return
            
        values = self.tree.item(selected_item)['values']
        self.clear_fields()
        
        self.name_entry.insert(0, values[1])
        self.desc_entry.insert(0, values[2])
        self.qty_entry.insert(0, values[3])
        self.min_qty_entry.insert(0, values[4])

    # --- Funções de Usuário ---

    def open_user_registration(self):
        """Abre uma nova janela para cadastrar um usuário."""
        UserRegistrationWindow(self)


class UserRegistrationWindow(tk.Toplevel):
    """Janela para o cadastro de novos usuários."""
    def __init__(self, master):
        super().__init__(master)
        self.title("Cadastrar Novo Usuário")
        self.geometry("300x300")
        self.transient(master)
        self.grab_set()

        tk.Label(self, text="Novo Usuário", font=("Arial", 14)).pack(pady=10)

        tk.Label(self, text="Usuário:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Senha:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Label(self, text="Perfil:").pack(pady=5)
        self.profile_var = tk.StringVar()
        profile_options = ["Comum", "Administrador"]
        self.profile_menu = ttk.Combobox(self, textvariable=self.profile_var, values=profile_options, state="readonly")
        self.profile_menu.set("Comum") # Padrão
        self.profile_menu.pack()
        
        tk.Button(self, text="Cadastrar", command=self.register_user).pack(pady=20)

    def register_user(self):
        """Realiza o cadastro do novo usuário no banco."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        profile = self.profile_var.get()

        if not username or not password or not profile:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self)
            return

        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Erro", f"O nome de usuário '{username}' já existe.", parent=self)
            conn.close()
            return
            
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash, profile) VALUES (?, ?, ?)",
            (username, password_hash, profile)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", f"Usuário '{username}' cadastrado com sucesso.", parent=self)
        self.destroy()

# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    app = StockControlApp()
    app.mainloop()