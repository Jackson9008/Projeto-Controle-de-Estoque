# app.py

import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db, init_db, hash_password


# ---  Aplicação Principal  ---

class StockControlApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Controle de Estoque")
        self.geometry("900x600")
        self.current_user = None

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        for widget in self.container.winfo_children():
            widget.destroy()

        if page_name == "LoginFrame":
            frame = LoginFrame(parent=self.container, controller=self)
        elif page_name == "MainFrame":
            frame = MainFrame(parent=self.container, controller=self)
        else:
            raise ValueError(f"Frame {page_name} não encontrado.")

        self.frames[page_name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def login_success(self, user_info):
        self.current_user = user_info
        self.show_frame("MainFrame")

    def logout(self):
        self.current_user = None
        self.show_frame("LoginFrame")

# --- Tela de Login ---

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Login do Sistema", font=("Arial", 16)).pack(pady=20)

        tk.Label(self, text="Usuário:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Senha:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Entrar", command=self.check_login).pack(pady=10)

        self.bind_all("<Return>", lambda event: self.check_login())

    def check_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Erro", "Usuário e senha não podem estar vazios.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, profile FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao acessar banco: {e}")
            return

        if user and user[2] == hash_password(password):
            user_info = {'id': user[0], 'username': user[1], 'profile': user[3]}
            self.controller.login_success(user_info)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

# --- Tela Principal ---

class MainFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", pady=10, padx=10)

        user_info = self.controller.current_user
        tk.Label(top_frame, text=f"Bem-vindo(a), {user_info['username']} ({user_info['profile']})", font=("Arial", 12)).pack(side="left")
        tk.Button(top_frame, text="Sair", command=self.controller.logout).pack(side="right")

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=10, pady=5)

        management_frame = tk.Frame(self)
        management_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_product_widgets(management_frame)
        self.create_user_widgets(management_frame)
        self.load_products()

    def create_product_widgets(self, parent):
        frame = ttk.LabelFrame(parent, text="Gerenciamento de Produtos")
        frame.pack(fill="both", expand=True, pady=10)

        form = tk.Frame(frame)
        form.pack(fill="x", padx=10, pady=5)

        tk.Label(form, text="Nome:").grid(row=0, column=0)
        self.name_entry = tk.Entry(form, width=30)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form, text="Descrição:").grid(row=1, column=0)
        self.desc_entry = tk.Entry(form, width=30)
        self.desc_entry.grid(row=1, column=1)

        tk.Label(form, text="Qtd.:").grid(row=0, column=2)
        self.qty_entry = tk.Entry(form, width=10)
        self.qty_entry.grid(row=0, column=3)

        tk.Label(form, text="Qtd. Mín.:").grid(row=1, column=2)
        self.min_qty_entry = tk.Entry(form, width=10)
        self.min_qty_entry.grid(row=1, column=3)

        buttons = tk.Frame(frame)
        buttons.pack(fill="x", pady=5)

        tk.Button(buttons, text="Adicionar", command=self.add_product).pack(side="left", padx=5)
        tk.Button(buttons, text="Atualizar", command=self.update_product).pack(side="left", padx=5)
        tk.Button(buttons, text="Excluir", command=self.delete_product).pack(side="left", padx=5)
        tk.Button(buttons, text="Limpar", command=self.clear_fields).pack(side="left", padx=5)

        columns = ('id', 'name', 'description', 'quantity', 'min_quantity')
        self.tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.column('id', width=30)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        self.tree.tag_configure('low_stock', background='salmon')

    def create_user_widgets(self, parent):
        frame = ttk.LabelFrame(parent, text="Usuários")
        frame.pack(fill="x", pady=10)
        if self.controller.current_user['profile'] == "Administrador":
            tk.Button(frame, text="Novo Usuário", command=self.open_user_registration).pack(pady=10)
        else:
            tk.Label(frame, text="Apenas administradores podem cadastrar usuários.").pack()

    def validate_fields(self):
        if not self.name_entry.get() or not self.qty_entry.get() or not self.min_qty_entry.get():
            messagebox.showerror("Erro", "Preencha os campos obrigatórios.")
            return False
        try:
            int(self.qty_entry.get())
            int(self.min_qty_entry.get())
            return True
        except:
            messagebox.showerror("Erro", "Qtd. e Qtd. Mín. devem ser inteiros.")
            return False

    def add_product(self):
        if not self.validate_fields():
            return
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, description, quantity, min_quantity) VALUES (?, ?, ?, ?)", (
            self.name_entry.get(), self.desc_entry.get(), int(self.qty_entry.get()), int(self.min_qty_entry.get())))
        conn.commit()
        conn.close()
        self.load_products()
        self.clear_fields()

    def update_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Erro", "Selecione um produto.")
            return
        if not self.validate_fields():
            return
        product_id = self.tree.item(selected)['values'][0]
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name=?, description=?, quantity=?, min_quantity=? WHERE id=?", (
            self.name_entry.get(), self.desc_entry.get(), int(self.qty_entry.get()), int(self.min_qty_entry.get()), product_id))
        conn.commit()
        conn.close()
        self.load_products()
        self.clear_fields()

    def delete_product(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Erro", "Selecione um produto.")
            return
        if messagebox.askyesno("Confirmar", "Deseja excluir este produto?"):
            product_id = self.tree.item(selected)['values'][0]
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            conn.close()
            self.load_products()
            self.clear_fields()

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, quantity, min_quantity FROM products")
        for row in cursor.fetchall():
            tags = ('low_stock',) if row[3] <= row[4] else ()
            self.tree.insert('', 'end', values=row, tags=tags)
        conn.close()

    def clear_fields(self):
        for widget in [self.name_entry, self.desc_entry, self.qty_entry, self.min_qty_entry]:
            widget.delete(0, 'end')
        self.tree.selection_remove(self.tree.selection())

    def on_item_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        values = self.tree.item(selected)['values']
        self.name_entry.delete(0, 'end')
        self.name_entry.insert(0, values[1])
        self.desc_entry.delete(0, 'end')
        self.desc_entry.insert(0, values[2])
        self.qty_entry.delete(0, 'end')
        self.qty_entry.insert(0, values[3])
        self.min_qty_entry.delete(0, 'end')
        self.min_qty_entry.insert(0, values[4])

    def open_user_registration(self):
        UserRegistrationWindow(self)

class UserRegistrationWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Novo Usuário")
        self.geometry("300x250")
        self.transient(master)
        self.grab_set()

        tk.Label(self, text="Usuário").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Senha").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Label(self, text="Perfil").pack(pady=5)
        self.profile_var = tk.StringVar()
        self.profile_box = ttk.Combobox(self, textvariable=self.profile_var, values=["Comum", "Administrador"], state="readonly")
        self.profile_box.set("Comum")
        self.profile_box.pack()

        tk.Button(self, text="Cadastrar", command=self.register_user).pack(pady=15)

    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        profile = self.profile_var.get()

        if not username or not password or not profile:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.", parent=self)
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Usuário já existe.", parent=self)
            conn.close()
            return

        cursor.execute("INSERT INTO users (username, password_hash, profile) VALUES (?, ?, ?)", (
            username, hash_password(password), profile))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", f"Usuário '{username}' cadastrado com sucesso!", parent=self)
        self.destroy()

# --- Execução Principal ---
if __name__ == "__main__":
    init_db()
    app = StockControlApp()
    app.mainloop()
