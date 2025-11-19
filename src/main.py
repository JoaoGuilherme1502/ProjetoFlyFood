from pathlib import Path
import time

from utils import limpar_terminal, leitura_arquivo_txt, converte_matriz_para_tsplib
from forca_bruta import algoritmo_forca_bruta
from menus import menu, menu_algoritmo_bruto, menu_algoritmo_genetico
from genetico import executar_algoritmo_genetico


def main():
    limpar_terminal()

    ROOT = Path(__file__).parent.parent

    arquivo_txt = ROOT / "dados" / "mapa_exemplo.txt"
    arquivo_tsp = ROOT / "dados" / "mapa_exemplo.tsp"

    matriz, pontos = leitura_arquivo_txt(arquivo_txt)

    converte_matriz_para_tsplib(arquivo_txt, arquivo_tsp)

    while True:
        escolha = menu(menu_algoritmo_bruto, menu_algoritmo_genetico)

        if escolha == "bruto":

            print("Em busca da solução...")
            inicio = time.time()
            todas_rotas, melhor_rota, melhor_dist = algoritmo_forca_bruta(pontos)
            fim = time.time()

            menu_algoritmo_bruto(
                matriz,
                todas_rotas,
                melhor_rota,
                melhor_dist,
                pontos,
                fim - inicio
            )

        elif escolha == "genetico":

            print("Em busca da solução...")

            inicio = time.time()
            melhor_rota, melhor_distancia = executar_algoritmo_genetico(
                arquivo_tsp,
                populacao_tam=200,
                geracoes=500,
                taxa_mutacao=0.1,
                torneio_k=3,
                elitismo=True
            )
            fim = time.time()

            tempo_execucao = fim - inicio

            menu_algoritmo_genetico(melhor_rota, melhor_distancia, tempo_execucao)


if __name__ == "__main__":
    main()
