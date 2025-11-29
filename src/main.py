from pathlib import Path  # Usada para facilitar o endereçamento
import time  # Usada para calcular o tempo das operações

from utils import limpar_terminal, leitura_arquivo_txt, converte_matriz_para_tsplib
from forca_bruta import algoritmo_forca_bruta
from menus import menu, menu_algoritmo_bruto, menu_algoritmo_genetico
from genetico import executar_algoritmo_genetico


def main():
    """
    Docstring para main:

    Aqui é onde iniciamos o código do projeto FlyFood.

    Esta função coordena a execução geral do sistema, incluindo:
    - Leituras e conversões de modelos de mapa
    - Exibição dos menus principais para escolha do algoritmo(força bruta ou genético)
    - Medição de tempo de execução
    - Exibição de resultados obtidos por cada algoritmo
    """

    limpar_terminal()

    ROOT = Path(__file__).parent.parent
    # Os aruivos de mapas utilizados em nosso sistema
    arquivo_txt = ROOT / "dados" / "mapa_exemplo.txt"
    arquivo_tsp = ROOT / "dados" / "mapa_exemplo.tsp"
    brazil58_tsp = ROOT / "dados" / "brazil58.tsp"

    matriz, pontos = leitura_arquivo_txt(arquivo_txt)

    converte_matriz_para_tsplib(arquivo_txt, arquivo_tsp)

    while True:
        escolha = menu(menu_algoritmo_bruto, menu_algoritmo_genetico)

        if escolha == "bruto":
            # Mensagem de aguardo
            print("Em busca da solução...")
            inicio = time.time()  # Inicio da contagem da operação
            todas_rotas, melhor_rota, melhor_dist = algoritmo_forca_bruta(pontos)
            fim = time.time()  # FIm da contagem da operação

            menu_algoritmo_bruto(
                matriz,
                todas_rotas,
                melhor_rota,
                melhor_dist,
                pontos,
                fim - inicio
            ) # Passamento dos parâmetros

        elif escolha == "genetico":
            # Mensagem de aguardo
            print("Em busca da solução...")

            # é aqui que se realiza o balanceamento dos parâmetros e, escolha entre os arquivos: arquivo_tsp ou brazil58_tsp 
            populacao_tam = 500
            geracoes = 800
            taxa_mutacao = 0.15
            torneio_k = 3
            elitismo = True


            inicio = time.time()
            melhor_rota, melhor_distancia = executar_algoritmo_genetico(
                brazil58_tsp,
                populacao_tam,
                geracoes,
                taxa_mutacao,
                torneio_k,
                elitismo
            )  
            fim = time.time()

            tempo_execucao = fim - inicio

            menu_algoritmo_genetico(
                melhor_rota, 
                melhor_distancia, 
                tempo_execucao, 
                populacao_tam, 
                geracoes, 
                taxa_mutacao
            ) 


if __name__ == "__main__":
    main()
