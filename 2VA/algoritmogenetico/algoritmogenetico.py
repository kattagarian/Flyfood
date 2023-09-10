import numpy as np
import matplotlib.pyplot as plt
import math, random, time

def lerEntrada():
    arquivo = open('ch130.tsp')    #substituir por matriztsp7.tsp para entradas pequenas e berlin52.tsp para entradas grandes
    arquivo = arquivo.readlines()       #coloca cada linha em uma lista diferente
    aux = coords = []
    for i in range(6, len(arquivo)):    #começa o loop a partir da sexta linha onde começam as coordenadas
        aux = list(map(float, arquivo[i].split()))  #divide a linha em 3, indice da cidade, x e y
        coords.append([aux.pop(1), aux.pop(1)])     #remove o x e depois remove o y
    return coords

def matrizes(coords, qtdCidades):
    #Iniciar a matriz 52x52 com zeros
    matrizDistancia = np.zeros((qtdCidades, qtdCidades))
    for i in range(qtdCidades):
        for j in range(qtdCidades -1, i, -1):
            #Calcular cada distancia euclidiana entre as cidades e colocar o resultado na matriz
            matrizDistancia[i][j] = math.sqrt(((coords[i][0] - coords[j][0])**2) + ((coords[i][1] - coords[j][1])**2))
            #espelhar a matriz para que as duas metades tenham mesmos valores
            matrizDistancia[j][i] = matrizDistancia[i][j]
    return matrizDistancia

def plotIterDistancias(melhoresDistancias, geracoes, tamanho_populacao, taxa_mutacao):
    #plot das distâncias por geração
    plt.figure(figsize=(10, 6))
    plt.plot(melhoresDistancias, marker='o', linestyle='-', color='b')
    plt.xlabel('Geração')
    plt.ylabel('Melhor distância')
    plt.title(f'Melhores distâncias | Gerações: {geracoes}, Tamanho da População : {tamanho_populacao}, Taxa de Mutação: {taxa_mutacao}')
    plt.grid(True)
    #plt.show(block=False)
    plt.savefig("GAdistanciasgeracoes.png")

def plotCaminho(melhorRota_cidades, cidades, geracoes, tamanho_populacao, melhorDistancia, taxa_mutacao):
    #plot do melhor caminho
    plt.figure(figsize=(10, 6))
    plt.scatter(cidades[:, 0], cidades[:, 1], color='blue', label='Cidades')
    plt.plot(melhorRota_cidades[:, 0], melhorRota_cidades[:, 1], color='red', linewidth=2, label='Rota')
    for i, cidade in enumerate(melhorRota_cidades):
        plt.text(cidade[0], cidade[1], str(i), fontsize=12, color='black')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title(f'Melhor Solução: {melhorDistancia:.2f} | Gerações: {geracoes}, Tamanho da População : {tamanho_populacao}, Taxa de Mutação: {taxa_mutacao}')
    plt.grid(True)
    plt.savefig("GAplotCaminho.png")

# Function to generate a random caminho
def caminhoAleatorio(n):
    caminho = list(range(n))
    random.shuffle(caminho)
    return caminho

# Function to calculate the cost of a caminho
def fitness(caminho, matriz):
    custo = 0
    for i in range(len(caminho) - 1):
        custo += matriz[caminho[i]][caminho[i + 1]]
    custo += matriz[caminho[-1]][caminho[0]]
    return custo

# Function to perform selecao
def selecao(populacao, matriz):
    populacao = sorted(populacao, key=lambda x: fitness(x, matriz))
    aux = len(populacao)//2
    return populacao[:aux]

# Function to perform crossover
def crossover(pai1, pai2):
    geneA = random.randint(0, len(pai1))
    geneB = random.randint(0, len(pai1))
    comeco = min(geneA, geneB)
    fim = max(geneA, geneB)
    filho = [None] * len(pai1)
    filho[comeco:fim] = pai1[comeco:fim]

    for cidade in pai2:
        if cidade not in filho:
            i = filho.index(None)
            filho[i] = cidade
    return filho

# Function to perform mutacao
def mutacao(caminho, taxa_mutacao):
    if random.random() < taxa_mutacao:
        i = random.randint(0, len(caminho) - 1)
        j = random.randint(0, len(caminho) - 1)
        caminho[i], caminho[j] = caminho[j], caminho[i]
    return caminho

# Genetic algorithm function
def algoritmo_genetico(geracoes, tamanho_populacao, coords, matriz, taxa_mutacao):
    melhoresDistancias = []
    populacao = [caminhoAleatorio(len(coords)) for _ in range(tamanho_populacao)]
    for geracao in range(geracoes):
        populacao = selecao(populacao, matriz)
        novapopulacao = []
        for i in range(tamanho_populacao // 2):
            pai1, pai2 = random.sample(populacao, 2)
            filho = crossover(pai1, pai2)
            novapopulacao.append(mutacao(filho, taxa_mutacao))
        populacao += novapopulacao
        melhorCaminho = min(populacao, key=lambda x: fitness(x, matriz))
        #print(f"Geração {geracao}: Melhor Caminho = {fitness(melhorCaminho, matriz)}")
        melhoresDistancias.append(fitness(melhorCaminho, matriz))
    melhorCaminho = min(populacao, key=lambda x: fitness(x, matriz))
    melhorCaminho.append(melhorCaminho[0])
    return melhorCaminho, fitness(melhorCaminho, matriz), melhoresDistancias

def main():
    inicio = time.time()
    geracoes = 500 #quantas vezes o algoritmo será rodado
    tamanho_populacao = 200 #quantos indivíduos serão gerados
    taxa_mutacao = 1.0 #a probabilidade de um filho sofrer mutação
    coords = lerEntrada()   # entrada com as coordenadas da cidade
    cidades = np.array(coords)  #array em 2D com as coordenadas da cidade
    matriz = matrizes(coords, len(coords))  #matriz distancia

    melhorCaminho, melhorDistancia, melhoresDistancias = algoritmo_genetico(geracoes, tamanho_populacao, coords, matriz, taxa_mutacao)
    melhorRota_cidades = [cidades[i] for i in melhorCaminho]
    melhorRota_cidades = np.array(melhorRota_cidades)
    execucao = time.time() - inicio
    print(f"Melhor Distancia: {melhorDistancia:.2f} | Tempo: {execucao:.3f}s | gerações: {geracoes} | população: {tamanho_populacao} | mutação: {taxa_mutacao}")
    plotIterDistancias(melhoresDistancias, geracoes, tamanho_populacao, taxa_mutacao)
    plotCaminho(melhorRota_cidades, cidades, geracoes, tamanho_populacao, melhorDistancia, taxa_mutacao)

if __name__ == "__main__":
    main()
