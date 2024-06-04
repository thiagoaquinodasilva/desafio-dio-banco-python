import datetime
import os
import csv
import re

# Caminho para os arquivos
LOG_DIR = "Arquivo"
DADOS_FILE = "dados.csv"

# Função para criar diretório se não existir
def criar_diretorio():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

# Função para registrar log em arquivo
def registrar_log(log):
    criar_diretorio()
    with open(os.path.join(LOG_DIR, "log.txt"), "a") as file:
        file.write(log + "\n")

# Decorador para log de transações
def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log = f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. Retornou {resultado}"
        registrar_log(log)
        return resultado
    return envelope

# Classe Cliente unificada
class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ({self.cpf})>"

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao, valor):
        if conta.verificar_limite_transacoes():
            print("\n@@@ Você excedeu o número de transações permitidas para hoje! @@@")
            return False
        sucesso = transacao.registrar(conta, valor)
        if sucesso:
            conta.historico.adicionar_transacao(transacao)
        return sucesso

# Classe ContaCorrente unificada
class ContaCorrente:
    def __init__(self, agencia, numero, cliente, saldo_inicial=0, limite_saques=3, limite_saque_diario=500):
        self.agencia = agencia
        self.numero = numero
        self.cliente = cliente
        self.saldo = saldo_inicial
        self.historico = Historico()
        self.limite_saques = limite_saques
        self.numero_saques = 0
        self.limite_saque_diario = limite_saque_diario

    def __repr__(self):
        return f"<{self.__class__.__name__}: ('{self.agencia}', '{self.numero}', '{self.cliente.nome}')>"

    def verificar_limite_transacoes(self):
        return len(self.historico.transacoes_do_dia()) >= 10

    def depositar(self, valor):
        try:
            valor = float(valor)
            if valor <= 0:
                raise ValueError("O valor deve ser positivo.")
            self.saldo += valor
            print('\n=== Depósito realizado com sucesso! ===')
            return True
        except ValueError as e:
            print(f'\n@@@ Operação falhou! {e} @@@')
            return False

    def sacar(self, valor):
        try:
            valor = float(valor)
            if valor > self.saldo:
                raise ValueError("Saldo insuficiente.")
            if valor > self.limite_saque_diario:
                raise ValueError(f"O valor do saque excede o limite de R$ {self.limite_saque_diario}.")
            if self.numero_saques >= self.limite_saques:
                raise ValueError("Número máximo de saques diários excedido.")
            self.saldo -= valor
            self.numero_saques += 1
            print('\n=== Saque realizado com sucesso! ===')
            return True
        except ValueError as e:
            print(f'\n@@@ Operação falhou! {e} @@@')
            return False

    def exibir_extrato(self):
        print('\n================ EXTRATO ================')
        for transacao in self.historico.transacoes:
            print(transacao)
        print(f'\n  Saldo:          R$ {self.saldo:>7.2f}')
        print('========================================')


# Classe Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def transacoes_do_dia(self):
        hoje = datetime.datetime.now().date()
        return [t for t in self.transacoes if t.data_hora.date() == hoje]

class Deposito:
    @log_transacao
    def registrar(self, conta, valor):
        self.valor = valor
        self.data_hora = datetime.datetime.now()
        return conta.depositar(valor)

    def __str__(self):
        return f"  Depósito:   R$ {self.valor:>7.2f}          Dt. trans.:  {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"

class Saque:
    @log_transacao
    def registrar(self, conta, valor):
        self.valor = valor
        self.data_hora = datetime.datetime.now()
        return conta.sacar(valor)

    def __str__(self):
        return f"  Saque     :   R$ {self.valor:>7.2f}          Dt. trans.:  {self.data_hora.strftime('%d/%m/%Y %H:%M:%S')}"

# Funções auxiliares

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11

def validar_data_nascimento(data):
    return bool(re.match(r'\d{2}-\d{2}-\d{4}', data))

def criar_usuario(usuarios):
    try:
        cpf = input('Informe o CPF (somente número): ')
        if not validar_cpf(cpf):
            raise ValueError("CPF inválido. Deve conter 11 dígitos numéricos.")
        
        if filtrar_usuario(cpf, usuarios):
            raise ValueError("CPF já cadastrado.")

        data_nascimento = input('Informe a data de nascimento (dd-mm-aaaa):')
        if not validar_data_nascimento(data_nascimento):
            raise ValueError("Data de nascimento inválida. Deve estar no formato dd-mm-aaaa.")
        
        nome = input('Informe o nome completo: ')
        endereco = input('Informe o endereço (logradouro, nro - bairro - cidade/sigla estado)')
        novo_cliente = Cliente(nome, cpf, data_nascimento, endereco)
        usuarios.append(novo_cliente)
        salvar_dados(usuarios)  # Salvando dados unificados
        print('=== Usuário criado com sucesso! ===')
        return novo_cliente
    
    except ValueError as e:
        print(f'\n@@@ Erro: {e} @@@')

def criar_conta(agencia, numero_conta, usuario, usuarios):
    try:
        nova_conta = ContaCorrente(agencia, numero_conta, usuario)
        usuario.adicionar_conta(nova_conta)
        salvar_dados(usuarios)  # Salvando dados unificados
        print('\n=== Conta criada com sucesso! ===')
        return nova_conta
    except Exception as e:
        print(f'\n@@@ Erro ao criar conta: {e} @@@')

def listar_contas(contas):
    if not contas:
        print('\n@@@ Nenhuma conta encontrada! @@@')
        return
    print("=" * 100)
    print("LISTA DE CONTAS:")
    for conta in contas:
        print(f"Agência: {conta.agencia}\tConta: {conta.numero}\tTitular: {conta.cliente.nome}")
        print("-" * 100)

def salvar_dados(clientes):
    criar_diretorio()
    with open(os.path.join(LOG_DIR, DADOS_FILE), mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for cliente in clientes:
            for conta in cliente.contas:
                writer.writerow([cliente.nome, cliente.cpf, cliente.data_nascimento, cliente.endereco, conta.agencia, conta.numero, conta.saldo])

def carregar_dados():
    clientes = []
    dados_file_path = os.path.join(LOG_DIR, DADOS_FILE)
    if os.path.exists(dados_file_path):
        with open(dados_file_path, mode='r', newline='') as file:
            reader = csv.reader(file, delimiter=';', quotechar='"')
            for row in reader:
                if len(row) != 7:
                    continue
                nome, cpf, data_nascimento, endereco, agencia, numero, saldo = row
                cliente = filtrar_usuario(cpf, clientes)
                if not cliente:
                    cliente = Cliente(nome, cpf, data_nascimento, endereco)
                    clientes.append(cliente)
                conta = ContaCorrente(agencia, numero, cliente, float(saldo))
                cliente.adicionar_conta(conta)
    return clientes

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
    usuarios = carregar_dados()  # Carregando clientes e contas

    while True:
        opcao = menu()

        if opcao == 'd':
            numero_conta = input('Informe o número da conta: ')
            conta = next((conta for usuario in usuarios for conta in usuario.contas if str(conta.numero) == numero_conta), None)
            if conta:
                try:
                    valor = float(input('Informe o valor do depósito: '))
                    cliente = conta.cliente
                    cliente.realizar_transacao(conta, Deposito(), valor)
                    salvar_dados(usuarios)  # Salvar dados após a transação
                except ValueError:
                    print('\n@@@ Valor inválido! Por favor, insira um número. @@@')
            else:
                print('\n@@@ Conta não encontrada! @@@')

        elif opcao == 's':
            numero_conta = input('Informe o número da conta: ')
            conta = next((conta for usuario in usuarios for conta in usuario.contas if str(conta.numero) == numero_conta), None)
            if conta:
                valor = float(input('Informe o valor do saque: '))
                cliente = conta.cliente
                if cliente:
                    cliente.realizar_transacao(conta, Saque(), valor)
                    salvar_dados(usuarios)  # Salvar dados após a transação
                else:
                    print('\n@@@ Cliente não encontrado! @@@')
            else:
                print('\n@@@ Conta não encontrada! @@@')

        elif opcao == 'e':
            numero_conta = input('Informe o número da conta: ')
            conta = next((conta for usuario in usuarios for conta in usuario.contas if str(conta.numero) == numero_conta), None)
            if conta:
                conta.exibir_extrato()
            else:
                print('\n@@@ Conta não encontrada! @@@')

        elif opcao == 'nu':
            novo_usuario = criar_usuario(usuarios)
            if novo_usuario:
                numero_conta = len([conta for usuario in usuarios for conta in usuario.contas]) + 1
                criar_conta(AGENCIA, numero_conta, novo_usuario, usuarios)

        elif opcao == 'nc':
            cpf = input('Informe o CPF do usuário: ')
            usuario = filtrar_usuario(cpf, usuarios)
            if usuario:
                numero_conta = len(usuario.contas) + 1
                criar_conta(AGENCIA, numero_conta, usuario, usuarios)
            else:
                print('\n@@@ Usuário não encontrado! @@@')

        elif opcao == 'lc':
            listar_contas([conta for usuario in usuarios for conta in usuario.contas])

        elif opcao == 'q':
            break

if __name__ == '__main__':
    main()
