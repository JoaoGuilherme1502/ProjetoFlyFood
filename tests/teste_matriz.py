from itertools import permutations
from pathlib import Path
import os
import sys # Necessário para sys.exit()
import time

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
    """Apaga o terminal em qualquer sistema operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')

def distancia(p1, p2):
    """Calcula a distância Manhattan entre dois pontos (coordenadas)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def leitura_arquivo_txt(arquivo): 
    
    matriz = []
    pontos = {}
    
    try:
        with open(arquivo, "r") as f:
            linha_inicial = "" 
            while not linha_inicial:
                linha_inicial = f.readline().strip()
            
            if not linha_inicial:
                raise ValueError("O arquivo de mapa está vazio ou não possui dimensões.")
                
            linhas, colunas = map(int, linha_inicial.split())

            for _ in range(linhas):
                linha = f.readline().strip().split()
                matriz.append(linha)

        # Mapeamento dos pontos
        for i in range(linhas):
            for j in range(colunas):
                parte = matriz[i][j]
                if parte != "0":
                    pontos[parte] = (i + 1, j + 1)
        
        # A função deve retornar os dados lidos
        return matriz, pontos
    
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em {arquivo}")
        return None, None
    except Exception as e:
        print(f"Ocorreu um erro durante a leitura do arquivo: {e}")
        return None, None


def converte_matriz_para_tsplib(arquivo, output_file):
    nodes = []
    
    try:
        with open(arquivo, 'r') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            if len(lines) < 2:
                print("Erro: O arquivo de mapa não tem dados suficientes para conversão.")
                return

        grid_lines = lines[1:]
        node_id_counter = 1
        
        for row_index, line in enumerate(grid_lines):
            cells = line.split()
            for col_index, value in enumerate(cells):
                if value != '0':
                    nodes.append({
                        'id': node_id_counter,
                        'label': value, 
                        'x': float(col_index + 1),
                        'y': float(row_index + 1)
                    })
                    node_id_counter += 1

        #Escrita do Arquivo TSPLIB (.tsp)
        with open(output_file, 'w') as f:
            f.write(f"NAME: GridMap_Converted\n")
            f.write("TYPE: TSP\n")
            
            f.write("COMMENT: Mapeamento original -> ")
            mapping_str = ", ".join([f"{n['id']}={n['label']}" for n in nodes])
            f.write(f"{mapping_str}\n")
            
            f.write(f"DIMENSION: {len(nodes)}\n")
            f.write("EDGE_WEIGHT_TYPE: EUC_2D\n") 
            f.write("NODE_COORD_SECTION\n")
            
            for node in nodes:
                f.write(f"{node['id']} {node['x']:.1f} {node['y']:.1f}\n") 
            
            f.write("EOF\n")
            
        print(f"--- Conversão TSPLIB Concluída ---")
        print(f"Arquivo salvo em: {output_file}")
        
    except Exception as e:
        print(f"Ocorreu um erro na conversão TSPLIB: {e}")


def algoritmo_forca_bruta(pontos_mapa):
    """Calcula todas as permutações de rotas de entrega e encontra a melhor."""
    
    if not pontos_mapa:
        # Retorna valores vazios se não houver pontos
        return [], None, float("inf")

    entregas = [p for p in pontos_mapa.keys() if p != "R"]

    todas_rotas = []
    melhor_rota = None
    melhor_distancia = float("inf")

    # Garante que há pontos de entrega ou pelo menos o ponto R para uma rota simples
    if not entregas and "R" in pontos_mapa:
        rota_trivial = ["R", "R"]
        dist_trivial = distancia(pontos_mapa["R"], pontos_mapa["R"])
        return [(rota_trivial, dist_trivial)], rota_trivial, dist_trivial
    elif not entregas:
        return [], None, float("inf")


    for perm in permutations(entregas):
        rota = ["R"] + list(perm) + ["R"] 
        
        dist_total = sum(distancia(pontos_mapa[rota[i]], pontos_mapa[rota[i+1]]) 
                         for i in range(len(rota)-1))
        
        todas_rotas.append((rota, dist_total))

        if dist_total < melhor_distancia:
            melhor_distancia = dist_total
            melhor_rota = rota
    
    # A função deve retornar os resultados do cálculo
    return todas_rotas, melhor_rota, melhor_distancia


def menu(menu_algoritmo_bruto, menu_algoritmo_genetico):
    while True:
        limpar_terminal()
        print("="*50)
        print(" PROBLEMA DO CAIXEIRO VIAJANTE". center(50, "="))
        print("="*50)
        print("1 - Algoritmo Força Bruta")
        print("2 - Algoritmo Genético")
        
        escolha = input("Sua escolha: ").strip()

        if escolha == "1":
            limpar_terminal()
            menu_algoritmo_bruto
            break
        elif escolha == "2":
            limpar_terminal()
            menu_algoritmo_genetico
            break
        else:
            print("Opção inválida")
            limpar_terminal()


def menu_algoritmo_bruto(matriz, todas_rotas, melhor_rota, melhor_distancia, pontos, tempo_execucao):
    while True:
        limpar_terminal()
        print("="*50)
        print("ALGORITMO FORÇA BRUTA". center(50, "="))
        print("="*50)
        print("1 - Ver melhor rota")
        print("2 - Ver todas as rotas")
        print("3 - Ver ranking das rotas")
        print("4 - Visualizar matriz")
        print("5 - Sair")
        print("="*50)

        escolha = input("Escolha uma opção: ").strip()
        limpar_terminal()

        if escolha == "1":
            print("="*50)
            print("MELHOR ROTA ENCONTRADA".center(50))
            print("=" * 50)
            if melhor_rota:
                print(" -> ".join(melhor_rota))
                print(f"Distância total: {melhor_distancia}\nTempo de execução do programa: {tempo_execucao:.4f} segundos")
            else:
                print("Nenhum cálculo de rota realizado ou pontos insuficientes.")
            print("=" * 50)
            input("\nPressione ENTER para voltar ao menu...")
            limpar_terminal()

        elif escolha == "2":
            print("=" * 50)
            print("📍 TODAS AS ROTAS POSSÍVEIS".center(50))
            print("=" * 50)
            if len(pontos) <= 6: # limita a exibição de todas as rotas a 5 pontos
                if todas_rotas:
                    for idx, (rota, dist) in enumerate(todas_rotas, start=1):
                        print(f"{idx:02}. {' -> '.join(rota):<35} | Distância: {dist}")
                else:
                    print("Nenhuma rota calculada.")
            else:
                print("O programa limita a exibição de até 5 pontos de entrega!")
            print("=" * 50)
            input("\nPressione ENTER para voltar ao menu...")
            limpar_terminal()

        elif escolha == "3":
            print("=" * 50)
            print("RANKING DAS MELHORES ROTAS".center(50))
            print("=" * 50)
            if todas_rotas:
                ordenadas = sorted(todas_rotas, key=lambda x: x[1])
                for pos, (rota, dist) in enumerate(ordenadas, start=1):
                    print(f"{pos:02}. {' -> '.join(rota):<35} | Distância: {dist}")
            else:
                print("Nenhuma rota calculada.")
            print("=" * 50)
            input("\nPressione ENTER para voltar ao menu...")
            limpar_terminal()

        elif escolha == "4":
            print("="*50)
            print("MATRIZ LIDA".center(50))
            print("="*50)
            if matriz:
                    for linha in matriz:
                        print(linha)
            else:
                print("Matriz não carregada.")
            input("\nPressione ENTER para voltar ao menu...")
            limpar_terminal()

        elif escolha == "5":
            print("Saindo...")
            sys.exit(0) # Encerra o programa de forma limpa

        else:
            print("Opção inválida! Tente novamente.")
            input("Pressione ENTER para continuar...")
            limpar_terminal()



def menu_algoritmo_genetico():
    pass

def main():
    """
    Função principal que coordena o fluxo do programa.
    """
    limpar_terminal()
    print("Iniciando o solucionador TSP...")

    # Caminho do arquivo
    ROOT_PATH = Path(__file__).parent.parent
    arquivo = ROOT_PATH / "dados" / "mapa_exemplo.txt"

    # Captura os valores retornados pela função de leitura
    matriz, pontos = leitura_arquivo_txt(arquivo)
    
    if matriz is None or pontos is None:
        print("Falha ao carregar dados. Encerrando.")
        return

    # Captura os valores retornados pela função de força bruta e o tempo de execução

    inicio = time.time()
    todas_rotas, melhor_rota, melhor_distancia = algoritmo_forca_bruta(pontos)
    fim = time.time()
    tempo_execucao = fim - inicio
    
    # Geração do arquivo TSPLIB
    converte_matriz_para_tsplib(arquivo, "mapa_exemplo.tsp")

    menu(menu_algoritmo_bruto, menu_algoritmo_genetico)

    # Inicia o menu_algoritmo_bruto, passando os resultados como argumentos

    menu_algoritmo_bruto(matriz, todas_rotas, melhor_rota, melhor_distancia, pontos, tempo_execucao)

if __name__ == "__main__":
    main()