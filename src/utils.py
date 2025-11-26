import os
from pathlib import Path

def limpar_terminal():
    """ Apaga o terminal em qualquer sistema operacional """
    os.system('cls' if os.name == 'nt' else 'clear') 

def distancia_manhattan(a, b):
    """ Calcula a distância manhattan entre dois pontos """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def leitura_arquivo_txt(arquivo):
    """
    Lê um arquivo de mapa no formato TXT.

    O arquivo deve conter:
    - Primeira linha: duas dimensões que são as linhas e colunas
    - Demais linhas é a matriz indicando pontos, onde "0" representa espaço vazio, R representa o restaurante e "A, B, ..." representam os pontos de entrega"
    """

    matriz = []  # lista de listas contendo o mapa
    pontos = {}  # dicionário mapeando cada ponto á sua coordenada(linha, coluna)
    try:
        with open(arquivo, "r") as f:
            # Evitando as linhas vazias(caso tenha) e pulando até a primeira linha útil
            linha_inicial = ""
            while not linha_inicial:
                linha_inicial = f.readline().strip()
            if not linha_inicial:
                raise ValueError("O arquivo de mapa está vazio ou não possui dimensões.")
            # A primeira linha do arquivo vem com: linhas, colunas
            linhas, colunas = map(int, linha_inicial.split())
            # Agora é feita a leitura do restante da matriz
            for _ in range(linhas):
                linha = f.readline().strip().split()
                matriz.append(linha)
        # Percorre a matriz e guarda apenas as partes diferentes de "0"
        for i in range(linhas):
            for j in range(colunas):
                parte = matriz[i][j]
                if parte != "0":
                    pontos[parte] = (i + 1, j + 1)
        return matriz, pontos
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado em {arquivo}")
        return None, None # sem linha, sem coluna
    except Exception as e:
        print(f"Ocorreu um erro durante a leitura do arquivo: {e}")
        return None, None

def converte_matriz_para_tsplib(arquivo_txt, output_file):
    """
    Converte o mapa TXT para um arquivo .tsp

    O arquivo gerado contém:
    - Formato TSPLIB 
        - NAME
        - TTYPE
        - DIMENSION
        EDGE_WEIGHT_TYPE
    - Mapeamento 
    """

    nodes = []
    try:
        # Lê o arquivo e apenas a linha com conteúdo
        with open(arquivo_txt, 'r') as f:
            lines = [l.rstrip("\n") for l in f if l.strip()]
            # O arquivo precisa ter pelo menos dimensões e 1 linha de mapa
            if len(lines) < 2:
                print("Erro: O arquivo de mapa não tem dados suficientes para conversão.")
                return
        # As dimensões são ignoradas
        grid_lines = lines[1:]
        node_id_counter = 1
        # Aqui percorre o mapa montando os nós que serão exportados no .tsp
        for row_index, line in enumerate(grid_lines):
            cells = line.split()
            for col_index, value in enumerate(cells):
                # Só adiciona como nó se não for "0"
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

        # Aqui começa a escrever o arquivo .tsp
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

def leitura_tsp(brazil58_tsp):
    """
    Lê um arquivo TSPLIB (.tsp) e monta:
    - lista de ids
    - coordenadas
    - matriz de distâncias
    - índice de cada nó
    """
    
    coords_raw = {}
    id_map_comment = {}
    leitura_coords = False
    leitura_edges = False
    edge_format = None
    edge_type = None
    dimension = None
    weights_values = []

    try:
        with open(brazil58_tsp, "r") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line:
                    continue

                upper = line.upper()
                # captura DIMENSION
                if upper.startswith("DIMENSION"):
                    try:
                        _, val = line.split(":", 1)
                        dimension = int(val.strip())
                    except Exception:
                        parts = line.split()
                        if len(parts) >= 2 and parts[-1].isdigit():
                            dimension = int(parts[-1])
                    continue

                # captura EDGE_WEIGHT_FORMAT
                if upper.startswith("EDGE_WEIGHT_FORMAT"):
                    try:
                        _, val = line.split(":", 1)
                        edge_format = val.strip().upper()
                    except Exception:
                        edge_format = line.split()[-1].upper()
                    continue

                # captura EDGE_WEIGHT_TYPE
                if upper.startswith("EDGE_WEIGHT_TYPE"):
                    try:
                        _, val = line.split(":", 1)
                        edge_type = val.strip().upper()
                    except Exception:
                        edge_type = line.split()[-1].upper()
                    continue

                # mapeamento via COMMENT "->"
                if upper.startswith("COMMENT") and "->" in line:
                    try:
                        parte = line.split("->", 1)[1].strip()
                        pares = [p.strip() for p in parte.split(",") if p.strip()]
                        for par in pares:
                            if "=" in par:
                                left, right = par.split("=", 1)
                                left = left.strip()
                                right = right.strip()
                                # tenta converter left para int (índice)
                                try:
                                    key = int(left)
                                except Exception:
                                    # se não for inteiro, ignore
                                    continue
                                id_map_comment[key] = right
                    except Exception:
                        pass
                    continue

                # Início de seção de coordenadas
                if upper == "NODE_COORD_SECTION":
                    leitura_coords = True
                    leitura_edges = False
                    continue

                # Início de seção de pesos
                if upper == "EDGE_WEIGHT_SECTION":
                    leitura_edges = True
                    leitura_coords = False
                    continue

                # Fim de arquivo
                if upper == "EOF":
                    break

                # Leitura de coordenadas
                if leitura_coords:
                    partes = line.split()
                    if len(partes) >= 3:
                        node_id_raw = partes[0]
                        # tenta mapear para id legível se existir mapeamento no COMMENT
                        try:
                            node_id_int = int(node_id_raw)
                            node_key = id_map_comment.get(node_id_int, str(node_id_int))
                        except Exception:
                            node_key = str(node_id_raw)
                        x = float(partes[1])
                        y = float(partes[2])
                        coords_raw[node_key] = (x, y)
                    continue

                # Leitura de valores da matriz de arestas (coleção de números)
                if leitura_edges:
                    # a seção pode ter números separados por espaços e possivelmente quebras de linha
                    partes = line.split()
                    for p in partes:
                        # pula caracteres não numéricos
                        try:
                            # pode ser inteiro ou float; guardamos como int se inteiro
                            if "." in p:
                                val = float(p)
                            else:
                                val = int(p)
                            weights_values.append(val)
                        except Exception:
                            # ignora tokens estranhos
                            pass
                    continue
                continue

    except FileNotFoundError:
        print(f"Arquivo .tsp não encontrado: {brazil58_tsp}")
        return [], {}, [], {}
    except Exception as e:
        print(f"Erro ao ler .tsp: {e}")
        return [], {}, [], {}

    # Validar dimensão
    if dimension is None:
        # se temos coords_raw, inferir dimensão
        if coords_raw:
            dimension = len(coords_raw)
        elif weights_values:
            # tenta inferir n a partir do número de valores (para UPPER_ROW)
            m = len(weights_values)
            # n*(n-1)/2 = m  -> n^2 - n - 2m = 0
            import math
            disc = 1 + 8*m
            n_est = int((1 + math.isqrt(disc)) // 2)
            if n_est * (n_est - 1) // 2 == m:
                dimension = n_est
            else:
                print("Não foi possível inferir DIMENSION do arquivo .tsp.")
                return [], {}, [], {}
        else:
            print("DIMENSION não encontrada e não há dados suficientes.")
            return [], {}, [], {}

    n = dimension

    # Se temos coords_raw -> construir matriz por Manhattan (ou EUC_2D se preferir).
    if coords_raw:
        ids_list = list(coords_raw.keys())
        idx_map = {node: i for i, node in enumerate(ids_list)}
        # construir matriz usando Manhattan (seguindo seu código original)
        dist_matrix = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                xi, yi = coords_raw[ids_list[i]]
                xj, yj = coords_raw[ids_list[j]]
                dist_matrix[i][j] = abs(xi - xj) + abs(yi - yj)
        return ids_list, coords_raw, dist_matrix, idx_map

    # Caso não haja coords_raw: usamos EDGE_WEIGHT_SECTION (valores explícitos)
    if not weights_values:
        # não há coordenadas nem matriz explícita
        print("Nenhuma coordenada nem seção de pesos encontrada no .tsp.")
        return [], {}, [], {}

    # Reconstruir matriz a partir de weights_values segundo edge_format
    dist_matrix = [[0]*n for _ in range(n)]
    if edge_format is None:
        # tenta inferir: se #valores == n*(n-1)/2 -> UPPER_ROW provável
        expected_upper = n*(n-1)//2
        if len(weights_values) == expected_upper:
            edge_format = "UPPER_ROW"
        elif len(weights_values) == n*n:
            edge_format = "FULL_MATRIX"
        else:
            # fallback
            edge_format = "UNKNOWN"

    if edge_format in ("UPPER_ROW", "UPPERDIAGROW", "UPPER_ROW"):
        # preencher triangular superior: para i=0..n-2, j=i+1..n-1
        idx = 0
        try:
            for i in range(n):
                for j in range(i+1, n):
                    val = weights_values[idx]
                    dist_matrix[i][j] = val
                    dist_matrix[j][i] = val
                    idx += 1
        except IndexError:
            print("Valores insuficientes em EDGE_WEIGHT_SECTION para UPPER_ROW.")
            return [], {}, [], {}
    elif edge_format == "FULL_MATRIX":
        # preencher linha a linha (n*n valores)
        if len(weights_values) < n*n:
            print("FULL_MATRIX: valores insuficientes.")
            return [], {}, [], {}
        idx = 0
        for i in range(n):
            for j in range(n):
                dist_matrix[i][j] = weights_values[idx]
                idx += 1
    else:
        # formatos não tratados explicitamente: tenta preencher simetricamente
        expected_upper = n*(n-1)//2
        if len(weights_values) == expected_upper:
            idx = 0
            for i in range(n):
                for j in range(i+1, n):
                    val = weights_values[idx]
                    dist_matrix[i][j] = val
                    dist_matrix[j][i] = val
                    idx += 1
        else:
            print(f"Formato EDGE_WEIGHT_FORMAT='{edge_format}' não suportado automaticamente.")
            return [], {}, [], {}

    # construir ids_list: se id_map_comment tem mapeamento para 1..n, usa; senão, usa '1'..'n'
    ids_list = []
    if id_map_comment:
        # id_map_comment keys são inteiros (indices 1..n) — preservar ordem 1..n
        for i in range(1, n+1):
            ids_list.append(id_map_comment.get(i, str(i)))
    else:
        ids_list = [str(i) for i in range(1, n+1)]

    idx_map = {node: i for i, node in enumerate(ids_list)}
    return ids_list, coords_raw, dist_matrix, idx_map


