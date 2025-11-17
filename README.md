# FlyFood – Algoritmo de força bruta para roteamento de drones

## Descrição do projeto
O FlyFood é um projeto acadêmico desenvolvido na Universidade Federal Rural de Pernambuco (UFRPE) com o objetivo de simular um sistema de entregas por drones autônomos em ambiente urbano.  
O algoritmo busca determinar a rota mais eficiente para um drone realizar múltiplas entregas e retornar ao ponto inicial, minimizando a distância total percorrida.

A solução é baseada no Problema do Caixeiro Viajante (TSP – Traveling Salesman Problem) e utiliza o método de força bruta para gerar todas as rotas possíveis e selecionar a de menor custo, utilizando a distância de Manhattan (movimentos apenas horizontais e verticais).

---

## Funcionamento do Algoritmo

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

## Estrutura do projeto

### 1. Requisitos
- Python 3.10+
- Nenhuma biblioteca externa é necessária.


### 2. Interatividade
Durante a execução, o programa exibe o menu:
```
1 - Ver melhor rota
2 - Ver todas as rotas
```
- A opção 1 mostra a rota ótima e seu custo total.  
- A opção 2 lista todas as rotas possíveis e suas distâncias.

---

## Exemplo de Saída

```
Matriz lida:
['0', '0', '0', '0', 'D']
['0', 'A', '0', '0', '0']
['0', '0', '0', '0', 'C']
['R', '0', 'B', '0', '0']

Pontos encontrados: {'D': (0, 4), 'A': (1, 1), 'C': (2, 4), 'R': (3, 0), 'B': (3, 2)}

1 - Ver melhor rota
2 - Ver todas as rotas
Sua escolha: 1

Melhor rota: R -> D -> C -> A -> B -> R
Distância total: 14
```

---

## Complexidade Computacional

- Geração de permutações: O(n!)
- Cálculo de distância por rota: O(n)
- Complexidade total: O(n!)

A abordagem é adequada apenas para instâncias pequenas (até cerca de 9 pontos), sendo inviável para grandes volumes de entregas.

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
