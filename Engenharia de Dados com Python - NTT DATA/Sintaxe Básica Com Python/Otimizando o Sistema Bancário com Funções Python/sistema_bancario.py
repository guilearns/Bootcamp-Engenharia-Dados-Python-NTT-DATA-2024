import os
from datetime import datetime as dt
import locale
import textwrap

locale.setlocale(locale.LC_TIME, "pt-BR")

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

def obter_data_hora():
    dia = dt.today().strftime('%d')
    mes = dt.today().strftime('%b').capitalize()
    ano = dt.today().strftime('%Y')
    horario = dt.today().strftime('%H:%M:%S')

    return f"{dia}/{mes}/{ano} {horario}"

def obter_maior_string(mensagens):
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

def exibir_mensagens(mensagens):
    for mensagem in mensagens:
        if type(mensagem) == list:
            for linha in mensagem:
                print(linha)
        else:
            print(mensagem)

def exibir_aviso(titulo, *mensagens):
    maior_mensagem = obter_maior_string(mensagens)
    print(titulo.center(len(maior_mensagem), "="))
    exibir_mensagens(mensagens)
    print("".center(len(maior_mensagem), "="))

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"{obter_data_hora()} | (+) Depósito: R$ {valor:.2f}\n"
        exibir_aviso(" AVISO ", "Operação de depósito realizado com sucesso!")

    else:
        exibir_aviso(" AVISO ", "Operação falhou! O valor informado deve ser maior que zero.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        exibir_aviso(" AVISO ", "Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        exibir_aviso(" AVISO ", "Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        exibir_aviso(" AVISO ", "Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"{obter_data_hora()} | (-) Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        exibir_aviso(" AVISO ", "Saque realizado com sucesso!")

    else:
        exibir_aviso(" AVISO ", "Operação falhou! O valor informado deve ser maior que zero.")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    exibir_aviso(" EXTRATO ", "Não foram realizadas movimentações." if not extrato else extrato.splitlines(), f"\nSaldo:\t\tR$ {saldo:.2f}")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        exibir_aviso(" AVISO ", "Já existe usuário com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    exibir_aviso(" AVISO ", "Usuário criado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário já cadastrado: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    exibir_aviso(" AVISO ", "Usuário não encontrado, fluxo de criação de conta encerrado!")


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            os.system('cls')
            try:
                valor = float(input("Informe o valor do depósito: "))
                saldo, extrato = depositar(saldo, valor, extrato)
            except:
                exibir_aviso(" AVISO ", "Operação falhou! O valor informado é inválido.")
            
        elif opcao == "s":
            os.system('cls')
            try:
                valor = float(input("Informe o valor do saque: "))

                saldo, extrato = sacar(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=LIMITE_SAQUES,
                )
            except:
                exibir_aviso(" AVISO ", "Operação falhou! O valor informado é inválido.")

        elif opcao == "e":
            os.system('cls')
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            os.system('cls')
            criar_usuario(usuarios)

        elif opcao == "nc":
            os.system('cls')
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "lc":
            os.system('cls')
            if contas == []:
                exibir_aviso(" AVISO ", "Não há contas registradas no momento.")
            listar_contas(contas)

        elif opcao == "q":
            print("\nÉ um grande prazer ter você como nosso cliente.\n\nAté a próxima!\n")
            break

        else:
            os.system('cls')
            exibir_aviso(" AVISO ", "Operação inválida, por favor selecione novamente a operação desejada.")

main()