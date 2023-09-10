import numpy as np
import matplotlib.pyplot as plt
import math, random, time

def lerEntrada():
    arquivo = open('berlin52.tsp')    #substituir por matriztsp7.tsp para entradas pequenas e berlin52.tsp para entradas grandes
    arquivo = arquivo.readlines()     #coloca cada linha em uma lista diferente
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

def plotIterDistancias(melhoresDistancias, alfa, beta, rho):
    #plot das distâncias por geração
    plt.figure(figsize=(10, 6))
    plt.plot(melhoresDistancias, marker='o', linestyle='-', color='b')
    plt.xlabel('Iteração')
    plt.ylabel('Melhor distância')
    plt.title(f'Melhores distâncias | alfa: {alfa}, beta: {beta}, rho: {rho}')
    plt.grid(True)
    #plt.show(block=False)
    plt.savefig(f"totalDistanciasA{alfa}b{beta}rho{rho}f{formigas}i{iteracoes}.png")

def plotCaminho(melhorRota_cidades, cidades, alfa, beta, rho):
    #plot do melhor caminho
    plt.figure(figsize=(10, 6))
    plt.scatter(cidades[:, 0], cidades[:, 1], color='blue', label='Cidades')
    plt.plot(melhorRota_cidades[:, 0], melhorRota_cidades[:, 1], color='red', linewidth=2, label='Rota')
    for i, city in enumerate(melhorRota_cidades):
        plt.text(city[0], city[1], str(i), fontsize=12, color='black')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title(f'Melhor Solução: {melhorDistancia:.2f} | alfa: {alfa}, beta: {beta}, evaporação: {rho}, formigas: {formigas}, iteracoes: {iteracoes}')
    plt.grid(True)
    plt.savefig(f"caminhoa{alfa}b{beta}rho{rho}f{formigas}i{iteracoes}.png")

coords = lerEntrada()       #recebe a entrada
cidades = np.array(coords)  #array em 2D com as coordenadas da cidade
qtdCidades = len(coords)    #variável com a quantidade de cidades

'''#HYPERPARAMETROS TESTE
formigas = random.choice([10, 20, 30, 50, 100, 200])   #numero de formigas que percorrerão os caminhos a cada iteração default: 30
iteracoes = random.choice([50, 100, 200, 300, 500]) #numero de iteracoes a serem executadas default: 200
alfa = random.choice([1, 2, 3, 4, 5, 10, 15])     #quanto maior o alfa, mais o feromônio vai impactar default: 1
beta = random.choice([1, 2, 3, 4, 5, 10, 15])            #quanto maior o beta, mais a distância vai impactar default: 5
rho = random.choice([0, 0.001, 0.01, 0.05, 0.1, 0.2, 0.5])       #taxa de evaporação default: 0.5
Q = 100         #uma constante relacionada à quantidade de trilha deixada pelas formigas default: 100'''

#HIPERPARAMETROS BERLIN52
formigas = 20  #numero de formigas que percorrerão os caminhos a cada iteração default: 30
iteracoes = 50 #numero de iteracoes a serem executadas default: 200
alfa = 1        #quanto maior o alfa, mais o feromônio vai impactar default: 1
beta = 5        #quanto maior o beta, mais a distância vai impactar default: 5
rho = 0.5         #taxa de evaporação default: 0.5
Q = 100         #uma constante relacionada à quantidade de trilha deixada pelas formigas default: 100

'''#HIPERPARAMETROS ENTRADAS PEQUENAS
formigas = 10   #numero de formigas que percorrerão os caminhos a cada iteração default: 30
iteracoes = 50  #numero de iteracoes a serem executadas default: 200
alfa = 1        #quanto maior o alfa, mais o feromônio vai impactar default: 1
beta = 5        #quanto maior o beta, mais a distância vai impactar default: 5
rho = 0         #taxa de evaporação default: 0.5
Q = 100         #uma constante relacionada à quantidade de trilha deixada pelas formigas default: 100'''

matrizDistancia = matrizes(coords, len(coords))     #matriz com as distâncias entre as cidades
matrizFeromonio = np.ones((qtdCidades, qtdCidades)) #matriz com os feromonios entre cada cidade.
melhoresDistancias = []     #lista que vai guardar as melhores rotas de cada iteração
melhoresRotas = []          #lista com as melhores rotas
melhorRota = None           #inicializa variavel que vai armazenar a melhor rota global
melhorDistancia = float('inf')  #inicializa variavel com a melhor distancia global
passo = 0   #variavel pra calcular a porcentagem
inicio = time.time()

for i in range(iteracoes):
    caminhoFormiga = [] #a cada iteração zera a lista com o caminho das formigas
    caminhoFormigaDistancia = []    #zera as distancias percorridas pela formiga
    
    porcentagem = i/iteracoes   #função visual apenas para mostrar o progresso
    if(porcentagem >= passo):
        fim = time.time() - inicio
        print(f'{porcentagem*100}% iteração = {i} - {fim:.3f}s')
        passo += 0.1

    for formiga in range(formigas): #loop para cada formiga
        #formiga inicia de uma cidade aleatória
        cidadeAtual = random.randint(0, len(coords) -1) 
        #inicia lista com todas as cidades nao visitadas
        cidadeNaoVisitada = list(range(qtdCidades))
        #remove a primeira cidade da lista de cidades não visitadas
        cidadeNaoVisitada.remove(cidadeAtual)
        #adiciona a primeira cidade na lista de rota feita
        rota = [cidadeAtual]
        #inicializa a distancia total percorrida pela formiga
        distanciaTotal = 0
        #loop que vai rodar até a formiga percorrer cada cidade
        for _ in range(len(cidadeNaoVisitada)):
            #função probabilidade descrita no artigo do dorigo. esse é apenas o numerador
            probabilidade = (matrizFeromonio[cidadeAtual, cidadeNaoVisitada] ** alfa) * ((1.0 / matrizDistancia[cidadeAtual, cidadeNaoVisitada]) ** beta)
            #o denominador da função é o somatório do numerador. 
            probabilidade = probabilidade / sum(probabilidade)
            #escolhe a próxima cidade baseada na probabilidade de cada trecho
            proximaCidade = np.random.choice(cidadeNaoVisitada, p=probabilidade)
            #adiciona a próxima cidade escolhida na rota da formiga
            rota.append(proximaCidade)
            #adiciona a distância percorrida entre a cidade atual e a proxima cidade na variavel de distancia percorrida
            distanciaTotal += matrizDistancia[cidadeAtual, proximaCidade]
            #atualiza a cidade atual
            cidadeAtual = proximaCidade
            #remove a cidade atual das não visitadas
            cidadeNaoVisitada.remove(cidadeAtual)
        #no final da rota, adiciona o ponto inicial
        rota.append(rota[0])
        #adiciona a distancia da última cidade até a cidade inicial
        distanciaTotal += matrizDistancia[cidadeAtual, rota[0]]
        
        #armazena a rota feita
        caminhoFormiga.append(rota)
        #armazena a distância da rota percorrida
        caminhoFormigaDistancia.append(distanciaTotal)
        #verifica se a distancia percorrida pela formiga é a menor global
        if distanciaTotal < melhorDistancia:
            #se sim, pega a melhor distancia e melhor rota
            melhorDistancia = distanciaTotal
            melhorRota = rota
    
    #atualiza a matriz feromonio de acordo com a evaporação
    matrizFeromonio = matrizFeromonio * (1.0 - rho)
    for formiga, rota in enumerate(caminhoFormiga):
        for i in range(qtdCidades):
            matrizFeromonio[rota[i], rota[i + 1]] += Q / caminhoFormigaDistancia[formiga]

    #pega o indice da melhor rota
    indiceMelhorRota = np.argmin(caminhoFormigaDistancia)
    #usa o indice pra pegar a distancia correta
    melhoresDistancias.append(caminhoFormigaDistancia[indiceMelhorRota])
    melhoresRotas.append(caminhoFormiga[indiceMelhorRota])

execucao = time.time() - inicio
print(f"100.0% iteração = {iteracoes} - {execucao:.3f}s")

#cria um array 2d com as coordenadas da melhor rota
melhorRota_cidades = [cidades[i] for i in melhorRota]
melhorRota_cidades = np.array(melhorRota_cidades)
#imprime a melhor distancia
print(f'Melhor Distância: {melhorDistancia:.0f} | Tempo: {execucao:.3f}s')
#plot com as melhores distancias por iteracao
plotIterDistancias(melhoresDistancias, alfa, beta, rho)
#plot com o caminho feito
plotCaminho(melhorRota_cidades, cidades, alfa, beta, rho)
