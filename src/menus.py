import sys
from utils import limpar_terminal


# Variáveis globais para armazenar os resultados do AG
BEST_ROUTE = None
BEST_DISTANCE = None
AG_INFO = {}

def menu(menu_algoritmo_bruto, menu_algoritmo_genetico):
    while True:
        limpar_terminal()
        print("="*50)
        print(" PROBLEMA DO CAIXEIRO VIAJANTE ".center(50, "="))
        print("="*50)
        print("1 - Algoritmo Força Bruta")
        print("2 - Algoritmo Genético (ERX)")

        escolha = input("Sua escolha: ").strip()

        if escolha == "1":
            limpar_terminal()
            return "bruto"

        elif escolha == "2":
            limpar_terminal()
            return "genetico"

        else:
            print("Opção inválida!")
            input("Pressione ENTER para continuar...")


def menu_algoritmo_bruto(matriz, todas_rotas, melhor_rota, melhor_distancia, pontos, tempo_execucao):
    while True:
        limpar_terminal()
        print("="*50)
        print(" ALGORITMO FORÇA BRUTA ".center(50, "="))
        print("="*50)
        print("1 - Ver melhor rota")
        print("2 - Ver todas as rotas")
        print("3 - Ranking das rotas")
        print("4 - Visualizar matriz")
        print("5 - Voltar ao menu principal")

        escolha = input("Escolha uma opção: ").strip()
        limpar_terminal()

        if escolha == "1":
            print("="*50)
            print("MELHOR ROTA".center(50))
            print("="*50)
            print(" -> ".join(melhor_rota))
            print(f"Distância total: {melhor_distancia}")
            print(f"Tempo de execução: {tempo_execucao:.4f}s")
            input("\nPressione ENTER para voltar...")

        elif escolha == "2":
            print("="*50)
            print("TODAS AS ROTAS".center(50))
            print("="*50)
            if len(pontos) <= 6:
                for i, (rota, dist) in enumerate(todas_rotas, 1):
                    print(f"{i:02}. {' -> '.join(rota)} | Distância: {dist}")
            else:
                print("Limite de exibição (máx 6 pontos).")
            input("\nPressione ENTER...")

        elif escolha == "3":
            print("="*50)
            print("RANKING".center(50))
            print("="*50)
            ordenadas = sorted(todas_rotas, key=lambda x: x[1])
            for pos, (rota, dist) in enumerate(ordenadas, 1):
                print(f"{pos:02}. {' -> '.join(rota)} | Distância: {dist}")
            input("\nENTER para voltar...")

        elif escolha == "4":
            print("="*50)
            print("MATRIZ LIDA".center(50))
            print("="*50)
            for linha in matriz:
                print(linha)
            input("\nENTER para voltar...")

        elif escolha == "5":
            return

        else:
            print("Opção inválida!")
            input("ENTER para continuar...")


def menu_algoritmo_genetico(melhor_rota, melhor_distancia, tempo_execucao, populacao_tam, geracoes, taxa_mutacao):
    while True:
        limpar_terminal()
        print("="*50)
        print("ALGORITMO GENÉTICO (ERX)".center(50, "="))
        print("="*50)
        print("1 - Ver melhor solução encontrada")
        print("2 - Voltar ao menu principal")
        print("3 - Sair")
        print("="*50)

        escolha = input("Escolha uma opção: ").strip()
        limpar_terminal()

        if escolha == "1":
            print("=" * 50)
            print("MELHOR SOLUÇÃO ENCONTRADA".center(50))
            print("=" * 50)

            print("Rota:")
            print(" -> ".join(melhor_rota))

            print(f"\nDistância total: {melhor_distancia}")
            print(f"Tempo de execução: {tempo_execucao:.4f} segundos")
            print(f"Parâmetros utilizados:\nPopulação: {populacao_tam}\nGerações: {geracoes}\nTaxa: {taxa_mutacao}")

            print("=" * 50)
            input("\nPressione ENTER para voltar...")

        elif escolha == "2":
            return  # volta ao menu principal

        elif escolha == "3":
            sys.exit(0)

        else:
            print("Opção inválida!")
            input("\nPressione ENTER para continuar...")

    
