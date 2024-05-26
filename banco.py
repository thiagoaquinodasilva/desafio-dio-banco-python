import textwrap
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import os

# Caminho do arquivo de banco de dados
DB_FILE = 'contas.txt'

# Função para carregar contas do arquivo
def carregar_contas():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as file:
        linhas = file.readlines()
        contas = []
        for linha in linhas:
            agencia, numero, cpf, nome, data_nascimento, endereco = linha.strip().split(';')
            cliente = Cliente(nome, cpf, data_nascimento, endereco)
            conta = Conta(agencia, int(numero), cliente)
            contas.append(conta)
    return contas

# Função para salvar contas no arquivo
def salvar_conta(conta):
    with open(DB_FILE, 'a') as file:
        linha = f'{conta.agencia};{conta.numero};{conta.cliente.cpf};{conta.cliente.nome};{conta.cliente.data_nascimento};{conta.cliente.endereco}\n'
        file.write(linha)

# Classes adicionais conforme o diagrama UML
class Transacao(ABC):
    def __init__(self):
        self.data_hora = datetime.now()

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor

    def registrar(self, conta):
        conta.depositar(self.valor)

    def __str__(self):
        return f'Depósito:\tR$ {self.valor:.2f}\t{self.data_hora.strftime("%d-%m-%Y %H:%M:%S")}'

class Saque(Transacao):
    def __init__(self, valor):
        super().__init__()
        self.valor = valor

    def registrar(self, conta):
        return conta.sacar(self.valor)

    def __str__(self):
        return f'Saque:\t\tR$ {self.valor:.2f}\t{self.data_hora.strftime("%d-%m-%Y %H:%M:%S")}'

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def transacoes_do_dia(self):
        hoje = datetime.now().date()
        return [t for t in self.transacoes if t.data_hora.date() == hoje]

# Classes existentes atualizadas para interagir com as novas classes

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return False
        sucesso = transacao.registrar(conta)
        if sucesso:
            conta.historico.adicionar_transacao(transacao)
        return sucesso

class Conta:
    def __init__(self, agencia, numero, cliente, limite_saques=3):
        self.agencia = agencia
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0
        self.historico = Historico()
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print('\n=== Depósito realizado com sucesso! ===')
            return True
        else:
            print('\n@@@ Operação falhou! O valor informado é inválido. @@@')
            return False

    def sacar(self, valor):
        if valor > self.saldo:
            print('\n@@@ Operação falhou! Você não tem saldo suficiente. @@@')
            return False
        elif valor > 500:  # Supondo que 500 seja o limite de saque
            print('\n@@@ Operação falhou! O valor do saque excedeu o limite @@@')
            return False
        elif self.numero_saques >= self.limite_saques:
            print('\n@@@ Operação falhou! Número máximo de saques excedido @@@')
            return False
        elif valor > 0:
            self.saldo -= valor
            self.numero_saques += 1
            print('\n=== Saque realizado com sucesso! ===')
            return True
        else:
            print('\n@@@ Operação falhou! O valor informado é inválido. @@@')
            return False

    def exibir_extrato(self):
        print('\n=============== EXTRATO ===============')
        for transacao in self.historico.transacoes:
            print(transacao)
        print(f'\nSaldo:\t\tR$ {self.saldo:.2f}')
        print('=======================================')

# Funções auxiliares
def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente número): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('\n@@@ Já existe usuário com esse CPF! @@@')
        return None
    
    nome = input('Informe o nome completo: ')
    data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa):')
    endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado)')
    novo_usuario = Cliente(nome, cpf, data_nascimento, endereco)
    usuarios.append(novo_usuario)
    print('=== Usuário criado com sucesso! ===')
    return novo_usuario

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def criar_conta(agencia, numero_conta, usuario):
    nova_conta = Conta(agencia, numero_conta, usuario)
    usuario.adicionar_conta(nova_conta)
    salvar_conta(nova_conta)
    print('\n=== Conta criada com sucesso! ===')
    return nova_conta

def listar_contas(contas):
    if not contas:
        print('\n@@@ Nenhuma conta encontrada! @@@')
        return
    print("=" * 100)
    print("LISTA DE CONTAS:")
    for conta in contas:
        print(f"Agência: {conta.agencia}\tConta: {conta.numero}\tTitular: {conta.cliente.nome}")
        print("-" * 100)

# Implementação do menu e lógica principal
def menu():
    print("\n===== MENU =====")
    print("d - Realizar depósito")
    print("s - Realizar saque")
    print("e - Exibir extrato")
    print("nu - Novo usuário")
    print("nc - Nova conta para usuário existente")
    print("lc - Listar contas")
    print("q - Sair")
    return input("Escolha uma opção: ").lower()

def main():
    AGENCIA = '0001'
    usuarios = []
    contas = carregar_contas()

    while True:
        opcao = menu()

        if opcao == 'd':
            numero_conta = input('Informe o número da conta: ')
            conta = next((c for c in contas if str(c.numero) == numero_conta), None)
            if conta:
                valor = float(input('Informe o valor do depósito: '))
                cliente = conta.cliente
                cliente.realizar_transacao(conta, Deposito(valor))
            else:
                print('\n@@@ Conta não encontrada! @@@')
        
        elif opcao == 's':
            numero_conta = input('Informe o número da conta: ')
            conta = next((c for c in contas if str(c.numero) == numero_conta), None)
            if conta:
                valor = float(input('Informe o valor do saque: '))
                cliente = conta.cliente
                cliente.realizar_transacao(conta, Saque(valor))
            else:
                print('\n@@@ Conta não encontrada! @@@')

        elif opcao == 'e':
            numero_conta = input('Informe o número da conta: ')
            conta = next((c for c in contas if str(c.numero) == numero_conta), None)
            if conta:
                conta.exibir_extrato()
            else:
                print('\n@@@ Conta não encontrada! @@@')

        elif opcao == 'nu':
            novo_usuario = criar_usuario(usuarios)
            if novo_usuario:
                numero_conta = len(contas) + 1
                nova_conta = criar_conta(AGENCIA, numero_conta, novo_usuario)
                contas.append(nova_conta)

        elif opcao == 'nc':
            cpf = input('Informe o CPF do usuário: ')
            usuario = filtrar_usuario(cpf, usuarios)
            if usuario:
                numero_conta = len(contas) + 1
                nova_conta = criar_conta(AGENCIA, numero_conta, usuario)
                contas.append(nova_conta)
            else:
                print('\n@@@ Usuário não encontrado! @@@')

        elif opcao == 'lc':
            listar_contas(contas)

        elif opcao == 'q':
            break

if __name__ == '__main__':
    main()
