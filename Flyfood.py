import time
import matplotlib.pyplot as plt

def matriz(n_linhas, n_colunas, linhas):
    ponto_org, pontos_entr, coords = [], [], []
    # Pega os pontos e coordenadas
    for i in range(int(n_linhas)):
        linha = linhas[i].split()
        for j in range(int(n_colunas)):
            if linha[j] != '0':
                if linha[j] == 'R':
                    ponto_org.append([i, j])
                else:
                    coords.append([i, j])
                    pontos_entr.append(linha[j])
    return ponto_org, coords, pontos_entr

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
    #print(permutacoes)
    return permutacoes

# Calcula a distância entre os pontos
def distancia(pi, pj):
    dist = abs(pi[0] - pj[0]) + abs(pi[1] - pj[1])
    return dist

def custo(caminhos, ponto_org):
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
    return menor_custo, melhor_caminho

def main():
    comeco = time.time() #começa o contador de tempo
    arquivo = open('Matriz.txt', 'r') #input

    n_linhas, n_colunas = arquivo.readline().split() #recebe o numero de linhas e colunas
    linhas = arquivo.read().splitlines() #recebe as linhas
    ponto_org, coords, pontos_entr = matriz(n_linhas, n_colunas, linhas) #Chama a funcao matriz que retorna as coordenadas do ponto de inicio e dos pontos de entrega

    caminhos = permutacao(coords) #recebe todos os caminhos possiveis
    print(custo(caminhos, ponto_org)) #Recebe o menor custo e o caminho de menor custo em coordenadas
    tempo = time.time() - comeco # termina o contador de tempo
    print(f"O tempo de execução foi: {tempo} segundos")

if __name__ == "__main__":
    main()