# FlyFood – Algoritmo para roteamento de drones

## Descrição do projeto
O FlyFood é um projeto acadêmico desenvolvido na Universidade Federal Rural de Pernambuco (UFRPE) com o objetivo de simular um sistema de entregas por drones autônomos em ambiente urbano.  
O algoritmo busca determinar a rota mais eficiente para um drone realizar múltiplas entregas e retornar ao ponto inicial, minimizando a distância total percorrida.

A solução é baseada no Problema do Caixeiro Viajante (TSP – Traveling Salesman Problem) e oferece duas abordagens:

- Força Bruta - adequada para instâncias pequenas.
- Algoritmo Genético(AG) - ideal para intâncias médias ou grandes, incluindo arquivos TSPLIB.

---

## Funcionamento do Algoritmo de Força Bruta

1. Leitura da matriz urbana  
   O arquivo `mapa_exemplo.txt` contém a cidade representada por uma matriz.  
   O primeiro número indica o tamanho (linhas e colunas), seguido pelos pontos:
   - R → ponto de partida e retorno do drone (restaurante);
   - A, B, C, D → pontos de entrega;
   - 0 → espaços vazios.

   Exemplo de matriz:
   ```
   4 5
   0 0 0 0 D
   0 A 0 0 0
   0 0 0 0 C
   R 0 B 0 0
   ```

2. Identificação das coordenadas  
   O script lê o mapa e armazena as coordenadas de cada ponto em um dicionário Python.

3. Cálculo da distância Manhattan  
   Cada deslocamento entre dois pontos é calculado como:
   ```
   d(a, b) = |xa - xb| + |ya - yb|
   ```

4. Geração das rotas possíveis  
   O algoritmo utiliza itertools.permutations para criar todas as combinações possíveis das entregas.

5. Cálculo do custo total  
   Para cada rota, soma-se a distância entre os pontos consecutivos, retornando sempre ao ponto R.

6. Identificação da melhor rota  
   O algoritmo armazena a rota de menor custo total, exibindo-a ao final da execução.

---

## Funcionamente do Algoritmo Genético

O projeto inclui um AG completo com:
- Seleção por torneio
- Crossover ERX (Edge Recombination)
- Mutação por swap
- Elitismo opcional
- População, mutação e gerações configuráveis
  
Além disso, o AG tem suporte a variados formatos
- brazil58.tsp
- arquivo.tsp(convertido de um arquivo txt)

O leitor TSPLIB identifica:
- Nome
- Dimensão
- Coordenadas
- Estrutura do problema
Exemplo de trecho:

   NAME: brazil58

   TYPE: TSP
 
   DIMENSION: 58
 
   NODE_COORD_SECTION
 
   1 0 0
 
   2 14 3
 
   ...
   EOF
   
---

## Estrutura do projeto

### 1. Requisitos
- Python 3.10+
- Nenhuma biblioteca externa é necessária.


### 2. Execução
Rodar o programa no arquivo main.py
Durante a execução, o programa exibe o menu:
```
==================================================
========= PROBLEMA DO CAIXEIRO VIAJANTE ==========
==================================================
1 - Algoritmo Força Bruta
2 - Algoritmo Genético (ERX)
Sua escolha:
```
- A opção 1 mostra a rota ótima usando o Algoritmo de Força Bruta(não recomendado para mais de 12 pontos).  
- A opção 2 mostra o Algoritmo Genético(maior quantidade de pontos podem ser inseridos).

---

## Exemplo de Saída

```
1 - Ver melhor rota
...
Sua escolha: 1

Melhor rota: R -> D -> C -> A -> B -> R
Distância total: 14
Tempo de execução: 3.034 s
```

---

## Complexidade Computacional (Força Bruta)

- Geração de permutações: O(n!)
- Cálculo de distância por rota: O(n)
- Complexidade total: O(n!)

A abordagem é adequada apenas para instâncias pequenas (até cerca de 9 pontos), sendo inviável para grandes volumes de entregas.
Para instâncias maiores, recomenda-se o Algoritmo Genético

---

## Autores
- Igor Dias Vieira – igor.dvieira@ufrpe.br  
- João Guilherme Soares de Araujo – joao.soaresaraujo@ufrpe.br
- Vinícius de Oliveira Miranda – vinicius.oliveiram@ufrpe.br
- Heitor Filgueira Lins de Oliveira –  heitor.filgueiral@ufrpe.br  

---

## Licença
Este projeto é de uso educacional e segue as diretrizes acadêmicas da UFRPE.  
Sinta-se livre para estudar, modificar e reutilizar o código para fins de aprendizado.
