import random
from gptree import GPTree
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.cluster import v_measure_score
import copy
import csv
from collections import Counter
import os

def crossover(tree1, tree2, X, Y, variables, labels, max_depth, cross_better_worse):
    # Fitness dos pais:
    fit_parent1 = fitness(tree1, X, Y, variables, labels)
    fit_parent2 = fitness(tree2, X, Y, variables, labels)

    # Escolhendo nodulo da primeira árvore
    node1, parent1, position1, level1 = tree1.get_random_node_with_parent()
    
    # Escolhendo nodulo da segunda árvore
    node2, parent2, position2 = tree2.escolher_node_nivel(level1)
    #node2, parent2, position2, level2 = tree2.get_random_node_with_parent()
    
    # Realizando Crossover:
    if position2 == 'root':
        tree2 = node1
    elif position1 == 'left':
        parent2.left = node1
    else:
        parent2.right = node1
    if position1 == 'root':
        tree1 = node2
    elif position2 == 'left':
        parent1.left = node2
    else:
        parent1.right = node2
    
    # Fitness dos filhos:
    fit_child1 = fitness(tree1, X, Y, variables, labels)
    fit_child2 = fitness(tree2, X, Y, variables, labels)

    if fit_parent1 >= fit_child1:
        cross_better_worse[1] += 1
    else:
        cross_better_worse[0] += 1
    
    if fit_parent2 >= fit_child2:
        cross_better_worse[1] += 1
    else:
        cross_better_worse[0] += 1

def fitness(sol, X, Y, variables, labels):
    # Calculando distancias de um para todos
    dist_matrix = [[0 for _ in range(X.shape[0])]for _ in range(X.shape[0])]
    for i in range(len(dist_matrix)):
        line1 = X.iloc[i]
        for j in range(len(dist_matrix[i])):
            line2 = X.iloc[j]
            sub = [a - b for a, b in zip(line1, line2)]
            dictionary = dict(zip(variables, sub))
            dist_matrix[i][j] = sol.evaluate(dictionary)
            # if dist_matrix[i][j] == float('inf'):
            #     # print(f"matriz[{i}][{j}]", "\n")
            #     dist_matrix[i][j] = 0
    # print("MATRIZZZZZ")
    # print(dist_matrix)

    # Calculando Clusters
    clustering = AgglomerativeClustering(n_clusters=len(labels),metric='precomputed',linkage='average')
    clustering.fit_predict(dist_matrix)

    # Calculando Fitness
    return v_measure_score(Y,clustering.labels_)


def selection(population, tam_max_ind, tam_pop, p_mut, p_cross, k_tour, n_elite, variables, X, Y, labels, cross_better_worse):
    # Elitismo
    new_population = population[-n_elite:]
    new_population = copy.deepcopy(new_population)

    while len(new_population) < tam_pop:
        # Torneio
        winners = []
        for _ in range(2):
            candidates = []
            for _ in range(k_tour):
                candidates.append(random.choice(population))
            candidates.sort()
            winners.append(copy.deepcopy(candidates[-1]))
        
        # Aplicando operadores genéticos
        if random.random() < p_mut:
            winners[0].mutation()
        if random.random() < p_mut:
            winners[1].mutation()
        if random.random() < p_cross:
            crossover(winners[0], winners[1], X, Y, variables, labels, tam_max_ind, cross_better_worse)
            

        new_population.append(winners[0])
        new_population.append(winners[1])

        if len(new_population) > tam_pop:
            new_population.pop()
        
    return new_population

def many_repetitions(population):
    # Contando as ocorrências de cada elemento na lista
    counter = Counter(population)

    # Calculando a quantidade de indivíduos repetidos
    # Um "indivíduo repetido" é aquele que aparece mais de uma vez na lista
    repetitions = sum(1 for count in counter.values() if count > 1)
    return repetitions

def symbolic_regression(tam_pop, tam_max_ind, p_mut, p_cross, n_elite, k_tour, n_ger, variables, operators, X, Y, labels):
    # Gerando Pop Inicial(Método Ramped Half-and-Half)
    population = []
    depths = list(range(2,tam_max_ind+1))
    for i in range(int(tam_pop/2)):
        population.append(GPTree(random.choice(depths),variables,operators,method='full'))
        population.append(GPTree(random.choice(depths),variables,operators,method='grow'))
    
    # Avaliando Pop inicial (Fitness)
    for sol in population:
            sol.fitness = fitness(sol, X, Y, variables, labels)
    population.sort()

    # Iterações
    statistics = []
    for i in range(1,n_ger+1):
        stats_per_ger = []
        stats_per_ger.append(i)

        # Coletando estatisticas
        all_fitness = []
        for sol in population:
            all_fitness.append(sol.fitness)
        stats_per_ger.append(np.mean(all_fitness))
        stats_per_ger.append(np.std(all_fitness))
        stats_per_ger.append(population[-1].fitness)
        stats_per_ger.append(population[0].fitness)

        # Verificando indivíduos repetidos na população
        repetitions = many_repetitions(population)
        stats_per_ger.append(repetitions)

        # Seleção
        cross_better_worse = [0,0] # Variáveis para guardar os individuos melhores e piores que os pais após o crossover
        population = selection(population,tam_max_ind, tam_pop, p_mut, p_cross, k_tour, n_elite,variables, X, Y, labels, cross_better_worse)
        stats_per_ger.append(cross_better_worse[0])
        stats_per_ger.append(cross_better_worse[1])

        # Avaliando Nova Pop (Fitness)
        for sol in population:
            sol.fitness = fitness(sol, X, Y, variables, labels)
        population.sort()

        statistics.append(stats_per_ger)

        # Exibindo Estatisticas
        print(f"Iteração {stats_per_ger[0]}: ")
        print(f"Fitness Media: {stats_per_ger[1]}, ")
        print(f"Fitness STD: {stats_per_ger[2]}, ")
        print(f"Melhor Fitness: {stats_per_ger[3]}, ")
        print(f"Pior Fitness: {stats_per_ger[4]},")
        print(f"Qtd Repetidos: {stats_per_ger[5]},")
        print(f"Indv melhores que os pais: {stats_per_ger[6]},")
        print(f"Indv piores que os pais: {stats_per_ger[7]}.\n")
    
    # Caminho da pasta onde o CSV será salvo
    output_folder = 'results/var_n_ger'

    # Garante que a pasta existe, cria caso contrário
    os.makedirs(output_folder, exist_ok=True)

    # Caminho completo do arquivo com a pasta incluída
    file_path = os.path.join(output_folder, f'stats_n_ger{n_ger}.csv')

    # Salvando todas as estatísticas em um arquivo CSV ao final do loop
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Iteração', 'Fitness Média', 'Fitness STD', 'Melhor Fitness', 'Pior Fitness', 'Qtd Repetidos', 'Indv melhores que os pais', 'Indv piores que os pais'])  # Cabeçalhos
        writer.writerows(statistics)

    print("Estatísticas de Treino salvas!\n")

    return population