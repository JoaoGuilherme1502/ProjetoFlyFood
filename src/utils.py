import os
from pathlib import Path

def limpar_terminal():
    """ Apaga o terminal em qualquer sistema operacional """
    os.system('cls' if os.name == 'nt' else 'clear') 

def distancia_manhattan(a, b):
    """ Calcula a distância manhattan entre dois pontos """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def leitura_arquivo_txt(arquivo):
    """Lê o mapa TXT (formato que você já usa)."""
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
        for i in range(linhas):
            for j in range(colunas):
                parte = matriz[i][j]
                if parte != "0":
                    pontos[parte] = (i + 1, j + 1)
        return matriz, pontos
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em {arquivo}")
        return None, None
    except Exception as e:
        print(f"Ocorreu um erro durante a leitura do arquivo: {e}")
        return None, None

def converte_matriz_para_tsplib(arquivo_txt, output_file):
    """Converte o mapa TXT para um arquivo .tsp"""
    nodes = []
    try:
        with open(arquivo_txt, 'r') as f:
            lines = [l.rstrip("\n") for l in f if l.strip()]
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
        # determina caminho de saída
        out_path = Path(output_file)
        if not out_path.parent.exists():
            try:
                out_path.parent.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass
        with open(out_path, 'w') as f:
            f.write("NAME: GridMap_Converted\n")
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
    except Exception as e:
        print(f"Ocorreu um erro na conversão TSPLIB: {e}")

def leitura_tsp(arquivo_tsp):
    """Lê um arquivo .tsp"""
    coords_raw = {}
    id_map_comment = {}
    leitura_coords = False
    try:
        with open(arquivo_tsp, "r") as f:
            for line in f:
                texto = line.strip()
                if not texto:
                    continue
                if texto.upper().startswith("COMMENT:") and "->" in texto:
                    try:
                        parte = texto.split("->", 1)[1].strip()
                        pares = [p.strip() for p in parte.split(",")]
                        for par in pares:
                            if "=" in par:
                                left, right = par.split("=", 1)
                                id_map_comment[int(left.strip())] = right.strip()
                    except Exception:
                        pass
                if texto.upper().startswith("NODE_COORD_SECTION"):
                    leitura_coords = True
                    continue
                if leitura_coords:
                    if texto.upper() == "EOF":
                        break
                    partes = texto.split()
                    if len(partes) >= 3:
                        node_id_raw = partes[0]
                        try:
                            node_id_int = int(node_id_raw)
                            node_key = id_map_comment.get(node_id_int, str(node_id_int))
                        except Exception:
                            node_key = str(node_id_raw)
                        x = float(partes[1])
                        y = float(partes[2])
                        coords_raw[node_key] = (x, y)
    except FileNotFoundError:
        print(f"Arquivo .tsp não encontrado: {arquivo_tsp}")
        return [], {}, [], {}
    except Exception as e:
        print(f"Erro ao ler .tsp: {e}")
        return [], {}, [], {}

    ids_list = list(coords_raw.keys())
    idx_map = {node: i for i, node in enumerate(ids_list)}
    n = len(ids_list)
    dist_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            xi, yi = coords_raw[ids_list[i]]
            xj, yj = coords_raw[ids_list[j]]
            dist_matrix[i][j] = abs(xi - xj) + abs(yi - yj)
    return ids_list, coords_raw, dist_matrix, idx_map
