import tkinter as tk
from itertools import permutations
from pathlib import Path
import os


def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')  # Apaga o terminal em qualquer os

"""
    Aplicação criada para resolver o Problema do Caixeiro Viajante de forma bruta, calculando todas as rotas possíveis entre os pontos de entrega.

    O programa:
    - Lê um mapa a partir de um arquivo texto (mapa_exemplo.txt), onde cada parte representa um ponto da matriz.
      - "R" representa o ponto de partida que no nosso caso é um restaurante (rota inicial e final).
      - Letras ou números diferentes de "0" representam locais de entrega.
      - "0" representa espaços vazios (sem entrega).
    
    - Identifica as coordenadas (linha, coluna) de cada ponto relevante no mapa.

    - Calcula a distância Manhattan entre dois pontos, que é a soma das diferenças absolutas
      entre suas coordenadas (|x1 - x2| + |y1 - y2|).

    - Gera todas as permutações possíveis das entregas e monta rotas completas começando e
      terminando em "R".

    - Calcula a distância total de cada rota e determina qual delas possui o menor percurso.

    - Exibe:
        1. A melhor rota encontrada e sua distância total.
        2. Todas as rotas possíveis com suas respectivas distâncias (opção 2 no menu).

    Este algoritmo utiliza força bruta (brute force), ou seja, testa todas as combinações possíveis,
    sendo ideal para mapas pequenos, mas pouco eficiente para grandes quantidades de pontos.
"""

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')  # Apaga o terminal em qualquer os


# Calcular a distância agora
def distancia(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def leitura_arquivo_txt(arquivo, pontos):

    matriz = []
    pontos = {}

    # Leitura do arquivo e construção da matriz
    with open(arquivo, "r") as f:
        linha_inicial = "" # Ignorar as linhas antes dos números
        while not linha_inicial:
            linha_inicial = f.readline().strip()
        linhas, colunas = map(int, linha_inicial.split())

        for _ in range(linhas):
            linha = f.readline().strip().split()
            matriz.append(linha)

    for i in range(linhas):
        for j in range(colunas):
            parte = matriz[i][j]
            if parte != "0":
                pontos[parte] = (i+1, j+1)


def converte_matriz_para_tsplib(arquivo, output_file):
    nodes = []
    
    # 1. Leitura e Processamento do Grid
    with open(arquivo, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    # A primeira linha (dimensões) é pulada
    grid_lines = lines[1:]
    
    node_id_counter = 1
    
    for row_index, line in enumerate(grid_lines):
        cells = line.split()
        
        for col_index, value in enumerate(cells):
            if value != '0':
                # AJUSTE: Usar coordenadas baseadas em 1 (X=Coluna+1, Y=Linha+1)
                nodes.append({
                    'id': node_id_counter,
                    'label': value, 
                    'x': float(col_index + 1), # Coordenada X (Coluna)
                    'y': float(row_index + 1)  # Coordenada Y (Linha)
                })
                node_id_counter += 1

    # 2. Escrita do Arquivo TSPLIB (.tsp)
    with open(output_file, 'w') as f:
        # Cabeçalho Padrão
        f.write(f"NAME: GridMap_Converted\n")
        f.write("TYPE: TSP\n")
        
        f.write("COMMENT: Mapeamento original -> ")
        mapping_str = ", ".join([f"{n['id']}={n['label']}" for n in nodes])
        f.write(f"{mapping_str}\n")
        
        f.write(f"DIMENSION: {len(nodes)}\n")
        
        # Manter como EUC_2D se o resolvedor externo for padrão,
        # ou se você não se importar que ele use distância Euclidiana.
        f.write("EDGE_WEIGHT_TYPE: EUC_2D\n") 
        f.write("NODE_COORD_SECTION\n")
        
        # Coordenadas: ID X Y (Ex: 1 1.0 1.0)
        for node in nodes:
            # Usando .0 para garantir a saída no formato float
            f.write(f"{node['id']} {node['x']:.1f} {node['y']:.1f}\n") 
        
        f.write("EOF\n")
        
    # ... (Resto da função de exibição) ...
    print(f"--- Conversão Concluída ---")
    print(f"Pontos encontrados: {len(nodes)}")
    print(f"Arquivo salvo em: {output_file}")
    print("Mapeamento gerado:")
    for n in nodes:
       print(f"  ID {n['id']} = '{n['label']}' em ({n['x']:.1f}, {n['y']:.1f})")



def algoritmo_forca_bruta(pontos_mapa):
    # Gerar as permutações
    entregas = [p for p in pontos_mapa.keys() if p != "R"]

    todas_rotas = []
    melhor_rota = None
    melhor_distancia = float("inf")

    for perm in permutations(entregas):
        rota = ["R"] + list(perm) + ["R"]  # começa no R e termina no R
        dist_total = sum(distancia(pontos_mapa[rota[i]], pontos_mapa[rota[i+1]]) for i in range(len(rota)-1))
        
        # Armazena cada rota e distância
        todas_rotas.append((rota, dist_total))

        # Melhor rota
        if dist_total < melhor_distancia:
            melhor_distancia = dist_total
            melhor_rota = rota
    

# Exibição dos resultados 
def exibir_menu(matriz, todas_rotas, melhor_rota, melhor_distancia):
    while True:
        print("="*50)
        print(" PROBLEMA DO CAIXEIRO VIAJANTE". center(50, "="))
        print("="*50)
        print("1 - Ver melhor rota\n2 - Ver todas as rotas\n3 - Ver ranking das rotas\n4 - Visualizar matriz\n5 - Sair\n","="*50)
        escolha = int(input("Escolha uma opção: ").strip())
        limpar_terminal()

        if escolha == 1:
            print("="*50)
            print("🚀 MELHOR ROTA ENCONTRADA".center(50))
            print("=" * 50)
            print(" -> ".join(melhor_rota))
            print(f"Distância total: {melhor_distancia}")
            print("=" * 50)
            input("\nPressione ENTER para voltar ao menu...")
            limpar_terminal()
        elif escolha == 2:
            print("=" * 50)
            print("📍 TODAS AS ROTAS POSSÍVEIS".center(50))
            print("=" * 50)
            for idx, (rota, dist) in enumerate(todas_rotas, start=1):
                print(f"{idx:02}. {' -> '.join(rota):<35} | Distância: {dist}")
            print("=" * 50)
            input("\nPressione ENTER para voltar ao menu...")
            limpar_terminal()

        elif escolha == 3:
            ordenadas = sorted(todas_rotas, key=lambda x: x[1])
            print("=" * 50)
            print("🏆 RANKING DAS MELHORES ROTAS".center(50))
            print("=" * 50)
            for pos, (rota, dist) in enumerate(ordenadas, start=1):
                print(f"{pos:02}. {' -> '.join(rota):<35} | Distância: {dist}")
            print("=" * 50)
            input("\nPressione ENTER para voltar ao menu...")
            limpar_terminal()

        elif escolha == 4:
            print("="*50)
            print("MATRIZ LIDA".center(50))
            print("="*50)
            for linha in matriz:
                print(linha)
            input("\nPressione ENTER para voltar ao menu...")
            limpar_terminal()

        elif escolha == 5:
            print("Saindo... 👋")
            break

        else:
            print("⚠️ Opção inválida! Tente novamente.")
            input("Pressione ENTER para continuar...")
            limpar_terminal()


def main():
    limpar_terminal()

    # Caminho do arquivo
    ROOT_PATH = Path(__file__).parent
    arquivo = ROOT_PATH.parent / "dados" / "mapa_exemplo.txt"

    matriz, pontos = leitura_arquivo_txt(arquivo)

    converte_matriz_para_tsplib(arquivo, "mapa_exemplo.tsp")

    todas_rotas, melhor_rota, melhor_distancia = algoritmo_forca_bruta(pontos)

    exibir_menu(matriz, todas_rotas, melhor_rota, melhor_distancia)

if __name__ == "__main__":
    main()