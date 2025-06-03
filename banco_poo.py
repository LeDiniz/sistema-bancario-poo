import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Usuario:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def executar_operacao(self, conta, operacao):
        operacao.processar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class Pessoa(Usuario):
    def __init__(self, nome, nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf


class ContaBancaria:
    def __init__(self, numero, titular):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._titular = titular
        self._registro = Registro()

    @classmethod
    def criar_conta(cls, titular, numero):
        return cls(numero, titular)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def titular(self):
        return self._titular

    @property
    def registro(self):
        return self._registro

    def sacar(self, valor):
        if valor <= 0:
            print("\n Valor inválido para saque. ")
            return False
        if valor > self._saldo:
            print("\n Saldo insuficiente. ")
            return False
        self._saldo -= valor
        print("\n=== Saque efetuado com sucesso! ===")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("\n Valor inválido para depósito. ")
            return False
        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True


class ContaCorrente(ContaBancaria):
    def __init__(self, numero, titular, limite=500, max_saques=3):
        super().__init__(numero, titular)
        self._limite = limite
        self._max_saques = max_saques

    def sacar(self, valor):
        saques_realizados = len([t for t in self.registro.transacoes if t["tipo"] == "Saque"])
        if valor > self._limite:
            print("\n Limite de saque excedido. ")
        elif saques_realizados >= self._max_saques:
            print("\n Número máximo de saques atingido. ")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""
        Agência:\t{self.agencia}
        Conta:\t\t{self.numero}
        Titular:\t{self.titular.nome}
        """


class Registro:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar(self, operacao):
        self._transacoes.append({
            "tipo": operacao.__class__.__name__,
            "valor": operacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })


class Operacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def processar(self, conta):
        pass


class Saque(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def processar(self, conta):
        if conta.sacar(self.valor):
            conta.registro.adicionar(self)


class Deposito(Operacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def processar(self, conta):
        if conta.depositar(self.valor):
            conta.registro.adicionar(self)


def exibir_menu():
    texto_menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo cliente
    [q]\tSair
    => """
    return input(textwrap.dedent(texto_menu))


def localizar_cliente(cpf, clientes):
    return next((c for c in clientes if c.cpf == cpf), None)


def obter_conta(cliente):
    if not cliente.contas:
        print("\n Cliente não possui contas cadastradas. ")
        return None
    return cliente.contas[0]


def operacao_deposito(clientes):
    cpf = input("CPF do cliente: ")
    cliente = localizar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado. ")
        return

    valor = float(input("Valor para depósito: "))
    conta = obter_conta(cliente)

    if conta:
        cliente.executar_operacao(conta, Deposito(valor))


def operacao_saque(clientes):
    cpf = input("CPF do cliente: ")
    cliente = localizar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado. ")
        return

    valor = float(input("Valor para saque: "))
    conta = obter_conta(cliente)

    if conta:
        cliente.executar_operacao(conta, Saque(valor))


def mostrar_extrato(clientes):
    cpf = input("CPF do cliente: ")
    cliente = localizar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado. ")
        return

    conta = obter_conta(cliente)
    if not conta:
        return

    print("\n=========== EXTRATO ===========")
    if not conta.registro.transacoes:
        print("Sem movimentações.")
    else:
        for t in conta.registro.transacoes:
            print(f"{t['tipo']}: R$ {t['valor']:.2f}")
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("================================")


def cadastrar_cliente(clientes):
    cpf = input("Digite o CPF: ")
    if localizar_cliente(cpf, clientes):
        print("\n CPF já cadastrado. ")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (rua, número - bairro - cidade/UF): ")

    novo_cliente = Pessoa(nome=nome, nascimento=nascimento, cpf=cpf, endereco=endereco)
    clientes.append(novo_cliente)
    print("\n=== Cliente cadastrado com sucesso! ===")


def criar_nova_conta(num_conta, clientes, contas):
    cpf = input("CPF do titular: ")
    cliente = localizar_cliente(cpf, clientes)

    if not cliente:
        print("\n Cliente não encontrado. ")
        return

    conta = ContaCorrente.criar_conta(titular=cliente, numero=num_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")


def exibir_contas(contas):
    for conta in contas:
        print("=" * 50)
        print(textwrap.dedent(str(conta)))


def sistema_bancario():
    clientes = []
    contas = []

    while True:
        escolha = exibir_menu()

        if escolha == "d":
            operacao_deposito(clientes)
        elif escolha == "s":
            operacao_saque(clientes)
        elif escolha == "e":
            mostrar_extrato(clientes)
        elif escolha == "nu":
            cadastrar_cliente(clientes)
        elif escolha == "nc":
            criar_nova_conta(len(contas) + 1, clientes, contas)
        elif escolha == "lc":
            exibir_contas(contas)
        elif escolha == "q":
            break
        else:
            print("\n Opção inválida. Tente novamente. ")


sistema_bancario()
