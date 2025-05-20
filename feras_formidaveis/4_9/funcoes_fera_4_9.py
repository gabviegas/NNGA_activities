import random

###############################################################################
#                                Senha-Diferentes Tamanhos                                    #
###############################################################################


def gene_senha(letras_possiveis):
    """Sorteia uma letra.

    Args:
      letras: letras possíveis de serem sorteadas.

    """
    letra = random.choice(letras_possiveis)
    return letra


def cria_candidato_senha(tamanho_senha, letras_possiveis):
    """Cria um candidato para o problema da senha

    Args:
      tamanho_senha: inteiro representando o tamanho da senha.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    candidato = []

    for _ in range(tamanho_senha):
        candidato.append(gene_senha(letras_possiveis))

    return candidato


def populacao_senha_st(tamanho_populacao, tamanho_max_senha, letras_possiveis):
    """Cria população inicial no problema da senha

    Args
      tamanho_populacao: tamanho da população.
      tamanho_max_senha: inteiro representando o tamanho máximo da senha.
      letras_possiveis: letras possíveis de serem sorteadas.

    """
    populacao = []

    for _ in range(tamanho_populacao):
      tamanho_senha = random.randint(1,tamanho_max_senha+1)
      populacao.append(cria_candidato_senha(tamanho_senha, letras_possiveis))

    return populacao


def funcao_objetivo_senha_st(candidato, senha_verdadeira):
    """Computa a funcao objetivo de um candidato no problema da senha

    Args:
      candidato: um palpite para a senha que você quer descobrir
      senha_verdadeira: a senha que você está tentando descobrir

    """

    # cálculo da diferença entre tamanhos
    tamanho_senha_verdadeira = len(senha_verdadeira)
    tamanho_senha_canditado = len(candidato)

    distancia_tamanho = abs(tamanho_senha_canditado - tamanho_senha_verdadeira)

    distancia = 0

    for letra_candidato, letra_senha in zip(candidato, senha_verdadeira):
        num_letra_candidato = ord(letra_candidato)
        num_letra_senha = ord(letra_senha)
        distancia += abs(num_letra_candidato - num_letra_senha)

    return distancia + distancia_tamanho
 

def funcao_objetivo_pop_senha_st(populacao, senha_verdadeira):
    """Computa a funcao objetivo de uma populaçao no problema da senha.

    Args:
      populacao: lista contendo os individuos do problema
      senha_verdadeira: a senha que você está tentando descobrir

    """
    fitness = []

    for individuo in populacao:
        fitness.append(funcao_objetivo_senha_st(individuo, senha_verdadeira))

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

def cruzamento_ponto_simples_st(pai, mae, chance_de_cruzamento):
    """Realiza cruzamento de ponto simples levando em consideração tamanhos diferentes dos progenitores

    Args:
      pai: lista representando um individuo
      mae: lista representando um individuo
      chance_de_cruzamento: float entre 0 e 1 representando a chance de cruzamento

    """
    # define o range de corte levando em consideração o menor tamanho
    range_corte = min(len(pai), len(mae))

    if range_corte < 3:
      return pai, mae
    
    else:
      if random.random() < chance_de_cruzamento:
          corte = random.randint(1, range_corte - 2)
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
        vai_mutar = random.random() < chance_de_mutacao
        tem_tamanho = len(individuo)>2
        teste = vai_mutar & tem_tamanho
        if teste:
            gene = random.randint(0, len(individuo) - 1)
            valor_gene = individuo[gene]
            indice_letra = valores_possiveis.index(valor_gene)
            indice_letra += random.choice([1, -1])
            indice_letra %= len(valores_possiveis)
            individuo[gene] = valores_possiveis[indice_letra]
        else:
            pass

def mutacao_salto_tamanho(populacao,chance_de_mutacao,valores_possiveis):
    """Realiza mutação do tamanho por salto

      Args:
        populacao: lista contendo os indivíduos do problema
        chance_de_mutacao: float entre 0 e 1 representando a chance de mutação
        valores_possiveis: lista com todos os valores possíveis dos genes
      """
    for individuo in populacao:
        if random.random() < chance_de_mutacao:
            salto = random.choice([True,False])

            if salto and len(individuo)>1:
              individuo.pop(-1)
            
            else:
              letra = random.choice(valores_possiveis)
              individuo.append(letra)
