from itertools import permutations
from utils import distancia_manhattan

def algoritmo_forca_bruta(pontos_mapa):
   
    if not pontos_mapa:
        return [], None, float("inf")

    entregas = [p for p in pontos_mapa.keys() if p != "R"]
    todas_rotas = []
    melhor_rota = None
    melhor_distancia = float("inf")

    if not entregas and "R" in pontos_mapa:
        rota_trivial = ["R", "R"]
        dist_trivial = distancia_manhattan(pontos_mapa["R"], pontos_mapa["R"])
        return [(rota_trivial, dist_trivial)], rota_trivial, dist_trivial
    elif not entregas:
        return [], None, float("inf")

    for perm in permutations(entregas):
        rota = ["R"] + list(perm) + ["R"]
        dist_total = sum(distancia_manhattan(pontos_mapa[rota[i]], pontos_mapa[rota[i+1]])
                         for i in range(len(rota)-1))
        # inviavel com muitos pontos
        #todas_rotas.append((rota, dist_total))
        if dist_total < melhor_distancia:
            melhor_distancia = dist_total
            melhor_rota = rota

    return melhor_rota, melhor_distancia

