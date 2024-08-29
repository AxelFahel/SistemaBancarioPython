import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

# Banco de dados simples em memória
usuarios = {}
transacoes = []

# Função para criar um hash de senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para criar uma nova conta
def criar_conta(username, senha):
    if username in usuarios:
        messagebox.showerror("Erro", "Usuário já existe!")
        return False
    usuarios[username] = {
        "senha": hash_senha(senha),
        "contas": {}
    }
    messagebox.showinfo("Sucesso", f"Conta criada com sucesso para {username}!")
    return True

# Função para autenticar usuário
def autenticar(username, senha):
    if username in usuarios and usuarios[username]["senha"] == hash_senha(senha):
        return True
    else:
        messagebox.showerror("Erro", "Nome de usuário ou senha incorretos.")
        return False

# Função para criar uma nova conta bancária
def criar_conta_bancaria(username, tipo_conta):
    if tipo_conta in usuarios[username]["contas"]:
        messagebox.showerror("Erro", "Conta já existe!")
    else:
        usuarios[username]["contas"][tipo_conta] = 0
        messagebox.showinfo("Sucesso", f"Conta {tipo_conta} criada com sucesso!")

# Função para registrar transações
def registrar_transacao(username, tipo, valor, tipo_conta):
    transacao = {
        "usuario": username,
        "tipo": tipo,
        "valor": valor,
        "conta": tipo_conta,
        "data": datetime.datetime.now()
    }
    transacoes.append(transacao)

# Função para realizar depósito
def depositar(username, valor, tipo_conta):
    if tipo_conta in usuarios[username]["contas"]:
        usuarios[username]["contas"][tipo_conta] += valor
        registrar_transacao(username, "Depósito", valor, tipo_conta)
        messagebox.showinfo("Sucesso", f"Depósito de R$ {valor} realizado na conta {tipo_conta}!")
    else:
        messagebox.showerror("Erro", "Conta não existe.")

# Função para realizar saque
def sacar(username, valor, tipo_conta):
    if tipo_conta in usuarios[username]["contas"] and usuarios[username]["contas"][tipo_conta] >= valor:
        usuarios[username]["contas"][tipo_conta] -= valor
        registrar_transacao(username, "Saque", valor, tipo_conta)
        messagebox.showinfo("Sucesso", f"Saque de R$ {valor} realizado na conta {tipo_conta}!")
    else:
        messagebox.showerror("Erro", "Saldo insuficiente ou conta não existe.")

# Função para consultar saldo
def consultar_saldo(username, tipo_conta):
    if tipo_conta in usuarios[username]["contas"]:
        saldo = usuarios[username]["contas"][tipo_conta]
        messagebox.showinfo("Saldo", f"Seu saldo na conta {tipo_conta} é: R$ {saldo}")
    else:
        messagebox.showerror("Erro", "Conta não existe.")

# Função para exibir extrato
def exibir_extrato(username):
    extrato = ""
    for transacao in transacoes:
        if transacao["usuario"] == username:
            extrato += f"{transacao['data']} - {transacao['tipo']} ({transacao['conta']}): R$ {transacao['valor']}\n"
    if extrato:
        messagebox.showinfo("Extrato", extrato)
    else:
        messagebox.showinfo("Extrato", "Nenhuma transação encontrada.")

# Interface gráfica
class BancoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Bancário")
        self.geometry("400x300")
        self.username = None

        # Tela de login
        self.label_user = tk.Label(self, text="Usuário:")
        self.label_user.pack(pady=5)
        self.entry_user = tk.Entry(self)
        self.entry_user.pack(pady=5)

        self.label_pass = tk.Label(self, text="Senha:")
        self.label_pass.pack(pady=5)
        self.entry_pass = tk.Entry(self, show="*")
        self.entry_pass.pack(pady=5)

        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_login.pack(pady=5)

        self.button_register = tk.Button(self, text="Registrar", command=self.register)
        self.button_register.pack(pady=5)

    def login(self):
        username = self.entry_user.get()
        senha = self.entry_pass.get()
        if autenticar(username, senha):
            self.username = username
            self.show_main_menu()

    def register(self):
        username = self.entry_user.get()
        senha = self.entry_pass.get()
        criar_conta(username, senha)

    def show_main_menu(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.label_account = tk.Label(self, text=f"Bem-vindo, {self.username}")
        self.label_account.pack(pady=10)

        self.label_account_type = tk.Label(self, text="Tipo de Conta:")
        self.label_account_type.pack(pady=5)
        self.entry_account_type = tk.Entry(self)
        self.entry_account_type.pack(pady=5)

        self.button_create_account = tk.Button(self, text="Criar Conta Bancária", command=self.create_bank_account)
        self.button_create_account.pack(pady=5)

        self.button_deposit = tk.Button(self, text="Depositar", command=self.show_deposit_screen)
        self.button_deposit.pack(pady=5)

        self.button_withdraw = tk.Button(self, text="Sacar", command=self.show_withdraw_screen)
        self.button_withdraw.pack(pady=5)

        self.button_balance = tk.Button(self, text="Consultar Saldo", command=self.check_balance)
        self.button_balance.pack(pady=5)

        self.button_statement = tk.Button(self, text="Exibir Extrato", command=self.show_statement)
        self.button_statement.pack(pady=5)

    def create_bank_account(self):
        tipo_conta = self.entry_account_type.get()
        criar_conta_bancaria(self.username, tipo_conta)

    def show_deposit_screen(self):
        DepositScreen(self)

    def show_withdraw_screen(self):
        WithdrawScreen(self)

    def deposit(self, tipo_conta, valor):
        depositar(self.username, valor, tipo_conta)

    def withdraw(self, tipo_conta, valor):
        sacar(self.username, valor, tipo_conta)

    def check_balance(self):
        tipo_conta = self.entry_account_type.get()
        consultar_saldo(self.username, tipo_conta)

    def show_statement(self):
        exibir_extrato(self.username)

# Tela de Depósito
class DepositScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Depositar")
        self.geometry("300x200")

        self.label_account_type = tk.Label(self, text="Tipo de Conta:")
        self.label_account_type.pack(pady=5)
        self.entry_account_type = tk.Entry(self)
        self.entry_account_type.pack(pady=5)

        self.label_amount = tk.Label(self, text="Valor para Depósito:")
        self.label_amount.pack(pady=5)
        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack(pady=5)

        self.button_deposit = tk.Button(self, text="Confirmar", command=self.deposit)
        self.button_deposit.pack(pady=5)

    def deposit(self):
        tipo_conta = self.entry_account_type.get()
        valor = float(self.entry_amount.get())
        self.master.deposit(tipo_conta, valor)
        self.destroy()

# Tela de Saque
class WithdrawScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sacar")
        self.geometry("300x200")

        self.label_account_type = tk.Label(self, text="Tipo de Conta:")
        self.label_account_type.pack(pady=5)
        self.entry_account_type = tk.Entry(self)
        self.entry_account_type.pack(pady=5)

        self.label_amount = tk.Label(self, text="Valor para Saque:")
        self.label_amount.pack(pady=5)
        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack(pady=5)

        self.button_withdraw = tk.Button(self, text="Confirmar", command=self.withdraw)
        self.button_withdraw.pack(pady=5)

    def withdraw(self):
        tipo_conta = self.entry_account_type.get()
        valor = float(self.entry_amount.get())
        self.master.withdraw(tipo_conta, valor)
        self.destroy()

# Inicia a aplicação
if __name__ == "__main__":
    app = BancoApp()
    app.mainloop()
