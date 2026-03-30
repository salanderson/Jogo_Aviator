import random
import time
import os

def gerar_multiplicador():
    # Gera o crash baseado em uma distribuição simples
    # Quanto maior o número aleatório, maior o crash
    crash = 0.1 + (1 / random.random())
    return crash

def jogar_aviator():
    saldo = 1000  # saldo inicial fictício
    historico = []
    cont = 0
    
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("Histórico:", " | ".join(historico))
        print(f"Voou: {cont}X")
        print(f"Seu saldo: R$ {saldo:.2f}")
        try:
            if cont >= 20:
                historico = []
                cont = 0
                
            aposta = input("Digite sua aposta (0 para sair): ")
            aposta = float(aposta)
	
            if aposta == 0:
                print("Saindo...")
                break
            if aposta > saldo:
                print("Saldo insuficiente!")
                time.sleep(1)
                continue
            if aposta == "":
                print("Nao e permitido valor vazio!")
                time.sleep(1)
                continue
            
        except ValueError:
            print("Não e posivel apostar com valores vazio, digite um valor, caso nao tenha mais Saldo efetue uma recarga")
            
        saldo -= aposta
        
        crash = gerar_multiplicador()
        multiplicador = 0.1
        
        print("\n🛫 Iniciando rodada...")
        time.sleep(1)
        cont += 1
            
        while True:
            multiplicador += 0.01
            print(f"Voando: {multiplicador:.2f}x", end="\r")
            time.sleep(0.05)

            # Jogador quer fazer cashout?
            if multiplicador >= 1.1:  # evita cashout imediato
                if random.random() < 0.01:  # 2% de chance por tick de você apertar cashout (simulação)
                    ganho = aposta * multiplicador
                    saldo += ganho
                    historico.append("O")
                    print(f"\n💰 CASHOUT realizado: {ganho:.2f}")
                    time.sleep(2)
                    break

            # Crash chegou?
            if multiplicador >= crash:
                historico.append("X")
                print(f"\n💥 QUEBROU em {crash:.2f}x")
                time.sleep(2)
                break
                
        if saldo <= 0.99:
            print("Voce nao possui mais Credito sufiente para realizar uma aposta, efetue uma recarga")
            saldo = input("Digite o valor para recarregar: ")
            saldo = float(saldo)

        print("\n--- Fim da rodada ---")
        time.sleep(1)
jogar_aviator()
