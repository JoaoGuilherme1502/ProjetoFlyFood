from itertools import permutations
from pathlib import Path

# Caminho do arquivo
ROOT_PATH = Path(__file__).parent
arquivo = ROOT_PATH.parent / "dados" / "mapa_exemplo.txt"

# Leitura do arquivo e construção da matriz
with open(arquivo, "r") as f:
    linha_inicial = "" # Ignorar as linhas antes dos números
    while not linha_inicial:
        linha_inicial = f.readline().strip()
    linhas, colunas = map(int, linha_inicial.split())

    matriz = []
    for _ in range(linhas):
        linha = f.readline().strip().split()
        matriz.append(linha)

print("Matriz lida:")
for linha in matriz:
    print(linha)

pontos = {}
for i in range(linhas):
    for j in range(colunas):
        parte = matriz[i][j]
        if parte != "0":
            pontos[parte] = (i, j)

print(f"\nPontos encontrados: {pontos}")

# Calcular a distãncia agora
def distancia(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Gerar as permutações
entregas = [p for p in pontos.keys() if p != "R"]

todas_rotas = []
melhor_rota = None
melhor_distancia = float("inf")

for perm in permutations(entregas):
    rota = ["R"] + list(perm) + ["R"]  # começa no R e termina no R
    dist_total = sum(distancia(pontos[rota[i]], pontos[rota[i+1]]) for i in range(len(rota)-1))
    
    # Armazena cada rota e distância
    todas_rotas.append((rota, dist_total))

    # Melhor rota
    if dist_total < melhor_distancia:
        melhor_distancia = dist_total
        melhor_rota = rota
    

# Resultado 
while True:
    escolha = int(input("1 - Ver melhor rota\n2 - Ver todas as rotas\nSua escolha: ").strip())

    if escolha == 1:
        print("\nMelhor rota:", " -> ".join(melhor_rota))
        print("Distância total:", melhor_distancia)
    elif escolha == 2:
        for idx, (rota, dist) in enumerate(todas_rotas, start=1):
            print(f"{idx}. {" -> ".join(rota)} | Distância: {dist}")
    else:
        print("Insira uma opção válida!")
