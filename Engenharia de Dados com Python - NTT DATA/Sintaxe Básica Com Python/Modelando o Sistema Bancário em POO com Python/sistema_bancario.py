import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime as dt
import locale
import os


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

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
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            Avisos.exibir_aviso(" AVISO ", "Operação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            Avisos.exibir_aviso(" AVISO ", "Saque realizado com sucesso!")
            return True

        else:
            Avisos.exibir_aviso(" AVISO ", "Operação falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            Avisos.exibir_aviso(" AVISO ", "Depósito realizado com sucesso!")
        else:
            Avisos.exibir_aviso(" AVISO ", "Operação falhou! O valor informado é inválido.")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            Avisos.exibir_aviso(" AVISO ", "Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            Avisos.exibir_aviso(" AVISO ", "Operação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Avisos:

    @classmethod
    def obter_maior_string(cls, mensagens):
        maior_mensagem = ""
        for mensagem in mensagens:
            if type(mensagem) == list:
                for linha in mensagem:
                    if len(linha) > len(maior_mensagem):
                        maior_mensagem = linha
            else:
                if len(mensagem) > len(maior_mensagem):
                    maior_mensagem = mensagem
        return maior_mensagem

    @classmethod
    def exibir_mensagens(cls, mensagens):
        for mensagem in mensagens:
            if type(mensagem) == list:
                for linha in mensagem:
                    print(linha)
            else:
                print(mensagem)

    @classmethod
    def exibir_aviso(cls, titulo, *mensagens):
        maior_mensagem = cls.obter_maior_string(mensagens)
        print(titulo.center(len(maior_mensagem), "="))
        cls.exibir_mensagens(mensagens)
        print("".center(len(maior_mensagem), "="))


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def obter_data_hora(self):
        dia = dt.today().strftime('%d')
        mes = dt.today().strftime('%b').capitalize()
        ano = dt.today().strftime('%Y')
        horario = dt.today().strftime('%H:%M:%S')

        return f"{dia}/{mes}/{ano} {horario}"

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": self.obter_data_hora(),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        Avisos.exibir_aviso(" AVISO ", "Cliente não possui conta!")
        return

    quantidade_contas = len(cliente.contas)
    if quantidade_contas > 1:
        mensagem = "\nPor favor, digite o número de uma das contas abaixo:\n\n"
        for conta in cliente.contas:
            mensagem = mensagem + "C/C número: " + str(conta.numero) + "\n\n"
        mensagem = mensagem + "=> "
        while True:
            try:
                numero_da_conta = int(input(mensagem))
                if numero_da_conta >= 1 and numero_da_conta <= quantidade_contas:
                    break
                else:
                    Avisos.exibir_aviso(" AVISO ", "Por favor, digite o número de uma conta existente.")
            except:
                Avisos.exibir_aviso(" AVISO ", "Operação falhou! O valor informado é inválido.")
    return cliente.contas[numero_da_conta-1] if quantidade_contas > 1 else cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        Avisos.exibir_aviso(" AVISO ", "Cliente não encontrado!")
        return
    try:
        valor = float(input("Informe o valor do depósito: "))
        if valor > 0:
            transacao = Deposito(valor)

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                return

            cliente.realizar_transacao(conta, transacao)
        else:
            Avisos.exibir_aviso(" AVISO ", "Operação falhou! O valor informado deve ser maior que zero.")
    except:
        Avisos.exibir_aviso(" AVISO ", "Operação falhou! O valor informado é inválido.")


def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        Avisos.exibir_aviso(" AVISO ", "Cliente não encontrado!")
        return

    try:
        valor = float(input("Informe o valor do saque: "))
        if valor > 0:
            transacao = Saque(valor)

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                return

            cliente.realizar_transacao(conta, transacao)
        else:
            Avisos.exibir_aviso(" AVISO ", "Operação falhou! O valor informado deve ser maior que zero.")
    except:
        Avisos.exibir_aviso(" AVISO ", "Operação falhou! O valor informado é inválido.")

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        Avisos.exibir_aviso(" AVISO ", "Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f} | {transacao['data']}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        Avisos.exibir_aviso(" AVISO ", "Já existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    Avisos.exibir_aviso(" AVISO ", "Cliente criado com sucesso!")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        Avisos.exibir_aviso(" AVISO ", "Cliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    Avisos.exibir_aviso(" AVISO ", "Conta criada com sucesso!")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            os.system('cls')
            depositar(clientes)

        elif opcao == "s":
            os.system('cls')
            sacar(clientes)

        elif opcao == "e":
            os.system('cls')
            exibir_extrato(clientes)

        elif opcao == "nu":
            os.system('cls')
            criar_cliente(clientes)

        elif opcao == "nc":
            os.system('cls')
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            os.system('cls')
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            os.system('cls')
            Avisos.exibir_aviso(" AVISO ", "Operação inválida, por favor selecione novamente a operação desejada.")


main()