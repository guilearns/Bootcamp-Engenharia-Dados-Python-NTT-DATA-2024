### ATENÇÃO!
### Este é um desafio de Sintaxe Básica
### Por este motivo não foram utilizadas funções personalizadas e classes.

import os
from datetime import datetime as dt
import locale

locale.setlocale(locale.LC_TIME, "pt-BR")

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

print("Olá!\n\nAgradecemos a sua preferência na utilização do Py-Gui-Bank.")

while True:

    opcao = input(menu)

    if opcao == "D" or opcao == "d":
        os.system('cls')
        try:
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                dia = dt.today().strftime('%d')
                mes = dt.today().strftime('%b').capitalize()
                ano = dt.today().strftime('%Y')
                hora = dt.today().strftime('%H:%M:%S')

                saldo += valor
                extrato += f"{dia}/{mes}/{ano} {hora} | (+) Depósito: R$ {valor:.2f}\n"

            else:
                print("\n========================== AVISO ==========================")
                print("Operação falhou! O valor informado deve ser maior que zero.")
                print("===========================================================")
        except:
            print("\n========================== AVISO ==========================")
            print("Operação falhou! O valor informado é inválido.")
            print("===========================================================")

    elif opcao == "S" or opcao == "s":
        os.system('cls')
        try:
            valor = float(input("Informe o valor do saque: "))

            excedeu_saldo = valor > saldo

            excedeu_limite = valor > limite

            excedeu_saques = numero_saques >= LIMITE_SAQUES

            if excedeu_saldo:
                print("\n========================== AVISO ==========================")
                print("Operação falhou! Você não tem saldo suficiente.")
                print("===========================================================")

            elif excedeu_limite:
                print("\n========================== AVISO ==========================")
                print("Operação falhou! O valor do saque/dia excede o limite.")
                print("===========================================================")

            elif excedeu_saques:
                print("\n========================== AVISO ==========================")
                print("Operação falhou! Número máximo de saques/dia excedido.")
                print("===========================================================")

            elif valor > 0:
                dia = dt.today().strftime('%d')
                mes = dt.today().strftime('%b').capitalize()
                ano = dt.today().strftime('%Y')
                hora = dt.today().strftime('%H:%M:%S')
                saldo -= valor
                extrato += f"{dia}/{mes}/{ano} {hora} | (-) Saque: R$ {valor:.2f}\n"
                numero_saques += 1

            else:
                print("\n========================== AVISO ==========================")
                print("Operação falhou! O valor informado deve ser maior que zero.")
                print("===========================================================")
        except:
            print("\n========================== AVISO ==========================")
            print("Operação falhou! O valor informado é inválido.")
            print("===========================================================")

    elif opcao == "E" or opcao == "e":
        os.system('cls')
        print("\n===================== EXTRATO =====================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("===================================================")

    elif opcao == "Q" or opcao == "q":
        print("\nÉ um grande prazer ter você como nosso cliente.\n\nAté a próxima!\n")
        break

    else:
        os.system('cls')
        print("\n========================== AVISO ==========================")
        print("Operação inválida, por favor selecione novamente a operação desejada.")
        print("===========================================================")