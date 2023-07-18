import time

comeco = time.time()

arquivo = open('C:\\Users\\gutuc\\Desktop\\Matriz.txt', 'r')

n, m = arquivo.readline().split()
linhas = arquivo.read().splitlines()

ponto_org = []
pontos_entr = []
coords = []

# Pega os pontos e coordenadas
for i in range(int(n)):
    linha = linhas[i].split()
    for j in range(int(m)):
        if linha[j] != '0':
            if linha[j] == 'R':
                ponto_org.append([i, j])
            else:
                coords.append([i, j])
                pontos_entr.append(linha[j])

# print(ponto_org)
# print(pontos_entr)
# print(coords)

# Realiza a permutação dos pontos de entrega
def permutacao(pontos):
    if len(pontos) <= 1:
        return [pontos]
    permutacoes = []
    for index in range(len(pontos)):
        elem_fixo = pontos[index]
        lista_solta = pontos[:index] + pontos[index + 1:]
        for p in permutacao(lista_solta):
            permutacoes.append([elem_fixo] + p)
    return permutacoes

caminhos = permutacao(coords)
# print(caminhos)

# Calcula a distância entre os pontos
def distancia(pi, pj):
    dist = abs(pi[0] - pj[0]) + abs(pi[1] - pj[1])
    return dist

menor_custo = None
melhor_caminho = None

for caminho in caminhos:
    saida = distancia(ponto_org[0], caminho[0])
    volta = distancia(caminho[len(caminho)-1], ponto_org[0])
    custo = 0
    for ponto_i in range(len(caminho)-1):
        soma = distancia(caminho[ponto_i], caminho[ponto_i+1])
        custo += soma
    custo_total = custo + saida + volta
    if menor_custo == None:
        menor_custo = custo_total
    else:
        if custo_total < menor_custo:
            custo_total = menor_custo
            melhor_caminho = caminho

print(menor_custo, melhor_caminho)

# Pegando as posições do melhor caminho
# melher_perc = ''
# for posicao in melhor_caminho:
#     print(posicao)

fim = time.time()
tempo = (fim - comeco)
print(f"O tempo de execução foi: {tempo} segundos")