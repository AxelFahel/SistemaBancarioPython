import hashlib
import tkinter as tk
from tkinter import messagebox
import datetime

# Banco de dados simples em memória
usuarios = {}
transacoes = []

# Função para criar um hash de senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para verificar se uma conta bancária existe para um usuário
def conta_existe(username, tipo_conta):
    return tipo_conta in usuarios[username]["contas"]

# Função para exibir mensagens de erro
def exibir_erro(mensagem):
    messagebox.showerror("Erro", mensagem)

# Função para exibir mensagens de sucesso
def exibir_sucesso(mensagem):
    messagebox.showinfo("Sucesso", mensagem)

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

# Função para criar uma nova conta de usuário
def criar_conta(username, senha):
    if username in usuarios:
        exibir_erro("Usuário já existe!")
        return False
    usuarios[username] = {
        "senha": hash_senha(senha),
        "contas": {}
    }
    exibir_sucesso(f"Conta criada com sucesso para {username}!")
    return True

# Função para autenticar usuário
def autenticar(username, senha):
    if username in usuarios and usuarios[username]["senha"] == hash_senha(senha):
        return True
    exibir_erro("Nome de usuário ou senha incorretos.")
    return False

# Função para criar uma nova conta bancária
def criar_conta_bancaria(username, tipo_conta):
    if conta_existe(username, tipo_conta):
        exibir_erro("Conta já existe!")
    else:
        usuarios[username]["contas"][tipo_conta] = 0
        exibir_sucesso(f"Conta {tipo_conta} criada com sucesso!")

# Função para realizar depósito
def depositar(username, valor, tipo_conta):
    if conta_existe(username, tipo_conta):
        usuarios[username]["contas"][tipo_conta] += valor
        registrar_transacao(username, "Depósito", valor, tipo_conta)
        exibir_sucesso(f"Depósito de R$ {valor} realizado na conta {tipo_conta}!")
    else:
        exibir_erro("Conta não existe.")

# Função para realizar saque
def sacar(username, valor, tipo_conta):
    if conta_existe(username, tipo_conta) and usuarios[username]["contas"][tipo_conta] >= valor:
        usuarios[username]["contas"][tipo_conta] -= valor
        registrar_transacao(username, "Saque", valor, tipo_conta)
        exibir_sucesso(f"Saque de R$ {valor} realizado na conta {tipo_conta}!")
    else:
        exibir_erro("Saldo insuficiente ou conta não existe.")

# Função para consultar saldo
def consultar_saldo(username, tipo_conta):
    if conta_existe(username, tipo_conta):
        saldo = usuarios[username]["contas"][tipo_conta]
        exibir_sucesso(f"Seu saldo na conta {tipo_conta} é: R$ {saldo}")
    else:
        exibir_erro("Conta não existe.")

# Função para exibir extrato
def exibir_extrato(username):
    extrato = ""
    for transacao in transacoes:
        if transacao["usuario"] == username:
            extrato += f"{transacao['data']} - {transacao['tipo']} ({transacao['conta']}): R$ {transacao['valor']}\n"
    if extrato:
        exibir_sucesso(extrato)
    else:
        exibir_sucesso("Nenhuma transação encontrada.")

# Interface gráfica
class BancoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Bancário")
        self.geometry("400x300")
        self.username = None

        # Tela de login
        self.criar_tela_login()

    def criar_tela_login(self):
        self.limpar_tela()
        
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

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

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
        self.limpar_tela()

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
        self.show_transaction_screen("Depositar", self.deposit)

    def show_withdraw_screen(self):
        self.show_transaction_screen("Sacar", self.withdraw)

    def show_transaction_screen(self, title, command):
        TransactionScreen(self, title, command)

    def deposit(self, tipo_conta, valor):
        depositar(self.username, valor, tipo_conta)

    def withdraw(self, tipo_conta, valor):
        sacar(self.username, valor, tipo_conta)

    def check_balance(self):
        tipo_conta = self.entry_account_type.get()
        consultar_saldo(self.username, tipo_conta)

    def show_statement(self):
        exibir_extrato(self.username)

# Tela de Transação (Depósito/Saque)
class TransactionScreen(tk.Toplevel):
    def __init__(self, parent, title, command):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x200")
        self.command = command

        self.label_account_type = tk.Label(self, text="Tipo de Conta:")
        self.label_account_type.pack(pady=5)
        self.entry_account_type = tk.Entry(self)
        self.entry_account_type.pack(pady=5)

        self.label_amount = tk.Label(self, text="Valor:")
        self.label_amount.pack(pady=5)
        self.entry_amount = tk.Entry(self)
        self.entry_amount.pack(pady=5)

        self.button_confirm = tk.Button(self, text="Confirmar", command=self.process_transaction)
        self.button_confirm.pack(pady=5)

    def process_transaction(self):
        tipo_conta = self.entry_account_type.get()
        valor = float(self.entry_amount.get())
        self.command(tipo_conta, valor)
        self.destroy()

# Inicia a aplicação
if __name__ == "__main__":
    app = BancoApp()
    app.mainloop()
