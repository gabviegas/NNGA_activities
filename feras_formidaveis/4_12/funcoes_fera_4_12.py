import random

###############################################################################
#                                Palíndromos                                  #
###############################################################################


def gene_letra(letras_possiveis):
    """Sorteia uma letra.

    Args:
      letras: letras possíveis de serem sorteadas.

    """
    letra = random.choice(letras_possiveis)
    return letra


def cria_candidato_letra(tamanho_senha, letras_possiveis):
    """Cria um candidato para o problema da senha

    Args:
      tamanho_senha: inteiro representando o tamanho da senha.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    candidato = []

    for _ in range(tamanho_senha):
        candidato.append(gene_letra(letras_possiveis))

    return candidato


def populacao_palindromica(tamanho_populacao, tamanho_palindromo, letras_possiveis):
    """Cria população inicial no problema da senha

    Args
      tamanho_populacao: tamanho da população.
      tamanho_palindromo: inteiro representando o tamanho do palíndromo.
      letras_possiveis: letras possíveis de serem sorteadas.

    """

    populacao = []

    for _ in range(tamanho_populacao):
      populacao.append(cria_candidato_letra(tamanho_palindromo, letras_possiveis))

    return populacao


def funcao_objetivo_palindromo(candidato):
    """Computa a funcao objetivo de um candidato palindrômico

    Args:
      candidato: um possível palíndromo
    """

    distancia = 0

    candidato_set = set(candidato)
    vogais = set('aeiou')

    if candidato_set.intersection(vogais) == set(): distancia += 1
    if len(candidato_set) == 1: distancia += 1

    for letra_indo, letra_voltando in zip(candidato, candidato[::-1]):
        num_letra_candidato = ord(letra_indo)
        num_letra_senha = ord(letra_voltando)
        distancia += abs(num_letra_candidato - num_letra_senha)

    return distancia
 

def funcao_obj_pop_palindromos(populacao):
    """Computa a funcao objetivo de uma população palindrômica.

    Args:
      populacao: lista contendo os individuos do problema

    """
    fitness = []

    for individuo in populacao:
        fitness.append(funcao_objetivo_palindromo(individuo))

    return fitness

###############################################################################
#                                   Seleção                                   #
###############################################################################

def selecao_torneio_min(populacao, fitness, tamanho_torneio):
    """Faz a seleção de uma população usando torneio.

    Nota: da forma que está implementada, só funciona em problemas de
    minimização.

    Args:
      populacao: lista contendo os individuos do problema
      fitness: lista contendo os valores computados da funcao objetivo
      tamanho_torneio: quantidade de invíduos que batalham entre si

    """
    selecionados = []

    for _ in range(len(populacao)):
        sorteados = random.sample(populacao, tamanho_torneio)

        fitness_sorteados = []
        for individuo in sorteados:
            indice_individuo = populacao.index(individuo)
            fitness_sorteados.append(fitness[indice_individuo])

        min_fitness = min(fitness_sorteados)
        indice_min_fitness = fitness_sorteados.index(min_fitness)
        individuo_selecionado = sorteados[indice_min_fitness]

        selecionados.append(individuo_selecionado)

    return selecionados

###############################################################################
#                                Cruzamento                                   #
###############################################################################

def cruzamento_ponto_simples(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento de ponto simples

    Args:
      pai: lista representando um individuo
      mae: lista representando um individuo
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento

    """
    if random.random() < chance_de_cruzamento:
        corte = random.randint(1, len(mae) - 1)
        filho1 = pai[:corte] + mae[corte:]
        filho2 = mae[:corte] + pai[corte:]
        return filho1, filho2
    else:
        return pai, mae


###############################################################################
#                                   Mutação                                   #
###############################################################################


def mutacao_salto(populacao, chance_de_mutacao, valores_possiveis):
    """Realiza mutação de salto

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
      valores_possiveis: lista com todos os valores possíveis dos genes

    """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            indice_letra = valores_possiveis.index(valor_gene)
            indice_letra += random.choice([1, -1])
            indice_letra %= len(valores_possiveis)
            individuo[gene] = valores_possiveis[indice_letra]

def mutacao_simples_palindromica(populacao, chance_de_mutacao):
    """Realiza mutação simples palindrômica

    Args:
      populacao: lista contendo os indivíduos do problema
      chance_de_mutacao: float entre 0 e 1 representando a chance de mutação

    """
    for individuo in populacao:
        valores_possiveis = individuo
        if random.random() < chance_de_mutacao:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            valores_sorteio = set(valores_possiveis) - set([valor_gene])
            individuo[gene] = random.choice(list(valores_sorteio))
