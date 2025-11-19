import random
import time
from copy import deepcopy
from utils import leitura_tsp
from menus import BEST_ROUTE, BEST_DISTANCE, AG_INFO

def construir_tabela_arestas(p1, p2):
    tabela = {}
    tamanho = len(p1)

    for p in (p1, p2):
        for i in range(tamanho):
            nodo = p[i]
            esq = p[i - 1]
            dir = p[(i + 1) % tamanho]

            tabela.setdefault(nodo, set()).add(esq)
            tabela.setdefault(nodo, set()).add(dir)

    return tabela


def cruzamento_erx(pai1, pai2):
    tamanho = len(pai1)
    tabela = construir_tabela_arestas(pai1, pai2)
    tabela = {k: set(v) for k, v in tabela.items()}  # cópia segura

    atual = random.choice([pai1[0], pai2[0], random.choice(pai1)])
    filho = [atual]

    while len(filho) < tamanho:
        for viz in tabela.values():
            viz.discard(atual)

        vizinhos = tabela.get(atual, set())

        if vizinhos:
            menor = min(len(tabela[v]) for v in vizinhos)
            candidatos = [v for v in vizinhos if len(tabela[v]) == menor]
            prox = random.choice(candidatos)
        else:
            restantes = [n for n in pai1 if n not in filho]
            if not restantes:
                break
            prox = random.choice(restantes)

        filho.append(prox)
        atual = prox

    return filho


def mutacao_swap(individuo, taxa):
    if random.random() < taxa and len(individuo) >= 2:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]


def custo_rota(rota, deposito, mapa_idx, matriz_dist):
    total = 0

    if not rota:
        return 0

    dep_idx = mapa_idx[deposito]
    primeiro = mapa_idx[rota[0]]
    total += matriz_dist[dep_idx][primeiro]

    for i in range(len(rota)-1):
        a = mapa_idx[rota[i]]
        b = mapa_idx[rota[i+1]]
        total += matriz_dist[a][b]

    ultimo = mapa_idx[rota[-1]]
    total += matriz_dist[ultimo][dep_idx]

    return total


def executar_algoritmo_genetico(
    arquivo_tsp,
    populacao_tam=200,
    geracoes=500,
    taxa_mutacao=0.1,
    torneio_k=3,
    elitismo=True,
    seed=None
):
    global BEST_ROUTE, BEST_DISTANCE, AG_INFO

    if seed:
        random.seed(seed)

    ids, coords, matriz_dist, idx_map = leitura_tsp(arquivo_tsp)
    deposito = "R" if "R" in ids else ids[0]
    entregas = [n for n in ids if n != deposito]

    populacao = [random.sample(entregas, len(entregas)) for _ in range(populacao_tam)]

    melhor_global = None
    melhor_dist_global = float("inf")

    for g in range(geracoes):

        custos = {i: custo_rota(ind, deposito, idx_map, matriz_dist) for i, ind in enumerate(populacao)}

        melhor_idx = min(custos, key=custos.get)
        melhor_local = populacao[melhor_idx]
        melhor_local_dist = custos[melhor_idx]

        if melhor_local_dist < melhor_dist_global:
            melhor_dist_global = melhor_local_dist
            melhor_global = deepcopy(melhor_local)

        nova_pop = []

        if elitismo:
            nova_pop.append(deepcopy(melhor_local))

        def torneio():
            cand = random.sample(range(populacao_tam), torneio_k)
            return deepcopy(populacao[min(cand, key=lambda x: custos[x])])

        while len(nova_pop) < populacao_tam:
            p1 = torneio()
            p2 = torneio()
            filho = cruzamento_erx(p1, p2)
            mutacao_swap(filho, taxa_mutacao)
            nova_pop.append(filho)

        populacao = nova_pop

    melhor_rota_final = [deposito] + melhor_global + [deposito]

    return melhor_rota_final, melhor_dist_global
