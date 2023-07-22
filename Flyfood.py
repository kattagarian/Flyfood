from time import process_time_ns
import resource
# Pega os pontos e coordenadas
def matriz(n, m, linhas):
    ponto_org, coords = [], []
    for i in range(int(n)):
        linha = linhas[i].split()
        for j in range(int(m)):
            if linha[j] != '0':
                if linha[j] == 'R':
                    ponto_org.append([i, j])
                else:
                    coords.append(([i, j], linha[j]))
    return ponto_org, coords

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

# Calcula a distância entre os pontos
def distancia(pi, pj):
    dist = abs(pi[0] - pj[0]) + abs(pi[1] - pj[1])
    return dist

def custo(ponto_org, caminhos):
    menor_custo = None
    melhor_caminho = None
    for caminho in caminhos:
        saida = distancia(ponto_org[0], caminho[0][0])
        volta = distancia(caminho[len(caminho)-1][0], ponto_org[0])
        custo = 0
        for ponto_i in range(len(caminho)-1):
            soma = distancia(caminho[ponto_i][0], caminho[ponto_i+1][0])
            custo += soma
        custo_total = custo + saida + volta
        if menor_custo == None:
            menor_custo = custo_total
        else:
            if custo_total < menor_custo:
                menor_custo = custo_total
                melhor_caminho = caminho
    return melhor_caminho

def main():
    soma = 0
    for i in range(30):
        comeco = process_time_ns()
        arquivo = open('entrada10.txt', 'r')
        n, m = arquivo.readline().split()
        linhas = arquivo.read().splitlines()
        ponto_org, coords = matriz(n, m, linhas)    
        caminhos = permutacao(coords)
        melhor_caminho = custo(ponto_org, caminhos)
        #print([x[1] for x in melhor_caminho])

        fim = process_time_ns()
        #print(f"O tempo de execução foi: {fim - comeco} nanosegundos")
        soma = soma + (fim - comeco)
    print(f"A media foi: {soma/30}")
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
main()
