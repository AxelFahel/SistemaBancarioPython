import hashlib
import tkinter as tk
from tkinter import messagebox
import datetime

# Classe para representar uma Conta Bancária
class ContaBancaria:
    def __init__(self, tipo):
        self.tipo = tipo
        self.saldo = 0

    def depositar(self, valor):
        self.saldo += valor
        return f"Depósito de R$ {valor} realizado na conta {self.tipo}!"

    def sacar(self, valor):
        if self.saldo >= valor:
            self.saldo -= valor
            return f"Saque de R$ {valor} realizado na conta {self.tipo}!"
        return "Saldo insuficiente."

    def consultar_saldo(self):
        return f"Seu saldo na conta {self.tipo} é: R$ {self.saldo}"

# Classe para representar um Cliente
class Cliente:
    def __init__(self, username, senha):
        self.username = username
        self.senha = self.hash_senha(senha)
        self.contas = {}

    def hash_senha(self, senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def autenticar(self, senha):
        return self.senha == self.hash_senha(senha)

    def criar_conta_bancaria(self, tipo_conta):
        if tipo_conta in self.contas:
            return "Conta já existe!"
        self.contas[tipo_conta] = ContaBancaria(tipo_conta)
        return f"Conta {tipo_conta} criada com sucesso!"

    def obter_conta(self, tipo_conta):
        return self.contas.get(tipo_conta)

# Classe para representar o Banco
class Banco:
    def __init__(self):
        self.usuarios = {}
        self.transacoes = []

    def criar_conta(self, username, senha):
        if not username or not senha:
            return "Usuário ou senha não podem estar vazios!"
        if username in self.usuarios:
            return "Usuário já existe!"
        self.usuarios[username] = Cliente(username, senha)
        return f"Conta criada com sucesso para {username}!"

    def autenticar(self, username, senha):
        cliente = self.usuarios.get(username)
        if cliente and cliente.autenticar(senha):
            return True
        return "Nome de usuário ou senha incorretos."

    def criar_conta_bancaria(self, username, tipo_conta):
        if not tipo_conta:
            return "Tipo de conta não pode estar vazio!"
        cliente = self.usuarios.get(username)
        if cliente:
            return cliente.criar_conta_bancaria(tipo_conta)
        return "Usuário não encontrado."

    def depositar(self, username, valor, tipo_conta):
        if not valor or not tipo_conta:
            return "Valor e tipo de conta não podem estar vazios!"
        cliente = self.usuarios.get(username)
        if cliente:
            conta = cliente.obter_conta(tipo_conta)
            if conta:
                return conta.depositar(float(valor))
            return "Conta não existe."
        return "Usuário não encontrado."

    def sacar(self, username, valor, tipo_conta):
        if not valor or not tipo_conta:
            return "Valor e tipo de conta não podem estar vazios!"
        cliente = self.usuarios.get(username)
        if cliente:
            conta = cliente.obter_conta(tipo_conta)
            if conta:
                return conta.sacar(float(valor))
            return "Conta não existe."
        return "Usuário não encontrado."

    def consultar_saldo(self, username, tipo_conta):
        if not tipo_conta:
            return "Tipo de conta não pode estar vazio!"
        cliente = self.usuarios.get(username)
        if cliente:
            conta = cliente.obter_conta(tipo_conta)
            if conta:
                return conta.consultar_saldo()
            return "Conta não existe."
        return "Usuário não encontrado."

    def registrar_transacao(self, username, tipo, valor, tipo_conta):
        transacao = {
            "usuario": username,
            "tipo": tipo,
            "valor": valor,
            "conta": tipo_conta,
            "data": datetime.datetime.now()
        }
        self.transacoes.append(transacao)

    def exibir_extrato(self, username):
        extrato = ""
        for transacao in self.transacoes:
            if transacao["usuario"] == username:
                extrato += f"{transacao['data']} - {transacao['tipo']} ({transacao['conta']}): R$ {transacao['valor']}\n"
        return extrato if extrato else "Nenhuma transação encontrada."

# Estilizando a interface no estilo iOS
def configurar_estilo(widget):
    widget.config(
        bg="#ffffff",  # Fundo branco para melhor visibilidade
        fg="#000000",  # Texto preto
        font=("San Francisco", 12),  # Fonte similar ao iOS
        bd=0,  # Sem bordas para inputs
        highlightthickness=0  # Sem borda de destaque
    )
    if isinstance(widget, tk.Entry) or isinstance(widget, tk.Text):
        widget.config(relief="flat", highlightbackground="#d1d1d6", highlightcolor="#007aff")
    elif isinstance(widget, tk.Button):
        widget.config(
            bg="#007aff",  # Azul característico dos botões iOS
            fg="#ffffff",
            relief="flat",  # Botão sem borda
            bd=0,
            activebackground="#005fcb",
            activeforeground="#ffffff",
            highlightthickness=0,
            font=("San Francisco", 10, "bold")  # Fonte menor para botões menores
        )

class BancoApp(tk.Tk):
    def __init__(self, banco):
        super().__init__()
        self.banco = banco
        self.title("Sistema Bancário")
        self.geometry("400x350")
        self.config(bg="#f2f2f7")  # Fundo da janela

        self.username = None
        self.criar_tela_login()

    def criar_tela_login(self):
        self.limpar_tela()

        self.label_user = tk.Label(self, text="Usuário:")
        configurar_estilo(self.label_user)
        self.label_user.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_user = tk.Entry(self)
        configurar_estilo(self.entry_user)
        self.entry_user.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.label_pass = tk.Label(self, text="Senha:")
        configurar_estilo(self.label_pass)
        self.label_pass.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_pass = tk.Entry(self, show="*")
        configurar_estilo(self.entry_pass)
        self.entry_pass.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.button_login = tk.Button(self, text="Login", command=self.login)
        configurar_estilo(self.button_login)
        self.button_login.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.button_register = tk.Button(self, text="Registrar", command=self.register)
        configurar_estilo(self.button_register)
        self.button_register.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def validar_campos(self, *campos):
        for campo in campos:
            if not campo.get().strip():
                campo.config(bg="lightcoral")
                return False
            campo.config(bg="white")
        return True

    def login(self):
        if not self.validar_campos(self.entry_user, self.entry_pass):
            self.exibir_mensagem("Preencha todos os campos.")
            return

        username = self.entry_user.get()
        senha = self.entry_pass.get()
        result = self.banco.autenticar(username, senha)
        if result == True:
            self.username = username
            self.show_main_menu()
        else:
            self.exibir_mensagem(result)

    def register(self):
        if not self.validar_campos(self.entry_user, self.entry_pass):
            self.exibir_mensagem("Preencha todos os campos.")
            return

        username = self.entry_user.get()
        senha = self.entry_pass.get()
        result = self.banco.criar_conta(username, senha)
        self.exibir_mensagem(result)

    def show_main_menu(self):
        self.limpar_tela()

        self.label_account = tk.Label(self, text=f"Bem-vindo, {self.username}")
        configurar_estilo(self.label_account)
        self.label_account.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

        self.label_account_type = tk.Label(self, text="Tipo de Conta:")
        configurar_estilo(self.label_account_type)
        self.label_account_type.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_account_type = tk.Entry(self)
        configurar_estilo(self.entry_account_type)
        self.entry_account_type.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.button_create_account = tk.Button(self, text="Criar Conta", command=self.create_account)
        configurar_estilo(self.button_create_account)
        self.button_create_account.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.button_deposit = tk.Button(self, text="Depositar", command=self.deposit)
        configurar_estilo(self.button_deposit)
        self.button_deposit.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.button_withdraw = tk.Button(self, text="Sacar", command=self.withdraw)
        configurar_estilo(self.button_withdraw)
        self.button_withdraw.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.button_check_balance = tk.Button(self, text="Consultar Saldo", command=self.check_balance)
        configurar_estilo(self.button_check_balance)
        self.button_check_balance.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.button_statement = tk.Button(self, text="Extrato", command=self.show_statement)
        configurar_estilo(self.button_statement)
        self.button_statement.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Ajusta o grid para se expandir quando a janela for redimensionada
        self.grid_columnconfigure(1, weight=1)

    def create_account(self):
        if not self.validar_campos(self.entry_account_type):
            self.exibir_mensagem("Preencha todos os campos.")
            return

        tipo_conta = self.entry_account_type.get()
        result = self.banco.criar_conta_bancaria(self.username, tipo_conta)
        self.exibir_mensagem(result)

    def deposit(self):
        self.open_transaction_screen("Depósito", self.banco.depositar)

    def withdraw(self):
        self.open_transaction_screen("Saque", self.banco.sacar)

    def open_transaction_screen(self, title, command):
        transaction_screen = TransactionScreen(self, title, command)
        transaction_screen.transient(self)
        transaction_screen.grab_set()

    def check_balance(self):
        if not self.validar_campos(self.entry_account_type):
            self.exibir_mensagem("Preencha todos os campos.")
            return

        tipo_conta = self.entry_account_type.get()
        result = self.banco.consultar_saldo(self.username, tipo_conta)
        self.exibir_mensagem(result)

    def show_statement(self):
        extrato = self.banco.exibir_extrato(self.username)
        self.exibir_mensagem(extrato)

    def exibir_mensagem(self, mensagem):
        messagebox.showinfo("Informação", mensagem)

class TransactionScreen(tk.Toplevel):
    def __init__(self, parent, title, command):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x200")
        self.config(bg="#f2f2f7")  # Fundo da janela no estilo iOS
        self.command = command

        self.label_account_type = tk.Label(self, text="Tipo de Conta:")
        configurar_estilo(self.label_account_type)
        self.label_account_type.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry_account_type = tk.Entry(self)
        configurar_estilo(self.entry_account_type)
        self.entry_account_type.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.label_amount = tk.Label(self, text="Valor:")
        configurar_estilo(self.label_amount)
        self.label_amount.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entry_amount = tk.Entry(self)
        configurar_estilo(self.entry_amount)
        self.entry_amount.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.button_confirm = tk.Button(self, text="Confirmar", command=self.process_transaction)
        configurar_estilo(self.button_confirm)
        self.button_confirm.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Ajusta o grid para se expandir quando a janela for redimensionada
        self.grid_columnconfigure(1, weight=1)

    def process_transaction(self):
        if not self.validar_campos(self.entry_account_type, self.entry_amount):
            self.exibir_mensagem("Preencha todos os campos.")
            return

        tipo_conta = self.entry_account_type.get()
        valor = self.entry_amount.get()
        self.command(tipo_conta, valor)
        self.destroy()

    def validar_campos(self, *campos):
        for campo in campos:
            if not campo.get().strip():
                campo.config(bg="lightcoral")
                return False
            campo.config(bg="white")
        return True

    def exibir_mensagem(self, mensagem):
        messagebox.showinfo("Informação", mensagem)

# Inicia a aplicação
if __name__ == "__main__":
    banco = Banco()
    app = BancoApp(banco)
    app.mainloop()
