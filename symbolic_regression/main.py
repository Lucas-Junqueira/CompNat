from gptree import GPTree
from symb_reg import fitness
from symb_reg import symbolic_regression
import random
import pandas as pd
import numpy as np
import os
import csv

# Conseguindo Dados
data_train = pd.read_csv('/home/lucasjunq/Desktop/CompNat/data/breast_cancer_coimbra_train.csv')
data_test = pd.read_csv('/home/lucasjunq/Desktop/CompNat/data/breast_cancer_coimbra_test.csv')
X_train = data_train.loc[:, data_test.columns != 'Classification']
Y_train = data_train["Classification"]
Y_train = Y_train - 1
labels = Y_train.unique()
X_test = data_test.loc[:, data_test.columns != 'Classification']
Y_test = data_test["Classification"]
Y_test = Y_test - 1

variables = X_train.columns

# Definindo Parâmetros
operators = ['+','-','*','/','and','or','xor'] # Operadores
tam_pop = 100 # Tamanho da população inicial
n_ger = 50 # Números de gerações
p_mut = 0.6 # Probabilidade de mutação
p_cross = 0.3 # Probabilidade de CrossOver
# k_tour = 2 # Número K para o torneio
many_k_tour = [2, 5, 10, 25]
n_elite = 2 # Número de elitistas
tam_max_ind = 7 # Tamanho maximo do indivíduo

# Treino
#symbolic_regression(tam_pop,tam_max_ind,p_mut,p_cross,n_elite,k_tour,n_ger,variables,operators,X_train,Y_train, labels)

# Treino / Teste variando tamanho das gerações
for k_tour in many_k_tour:

    # Definindo semente aleatória
    random.seed(42)

    print(f"K DO TORNEIO: {k_tour}.\n")

    #Treino
    print("Estatisticas de Treino:\n")
    population = symbolic_regression(tam_pop,tam_max_ind,p_mut,p_cross,n_elite,k_tour,n_ger,variables,operators,X_train,Y_train, labels)

    # Teste
    print("Estatisticas de Teste:\n")

    for sol in population:
        sol.fitness = fitness(sol, X_test, Y_test, variables, labels)
    population.sort()

    all_fitness = []
    for sol in population:
        all_fitness.append(sol.fitness)
    test_stats = []
    test_stats.append(np.mean(all_fitness))
    test_stats.append(np.std(all_fitness))
    test_stats.append(population[-1].fitness)
    test_stats.append(population[0].fitness)
    
    print(f"Fitness Media: {test_stats[0]}, ")
    print(f"Fitness STD: {test_stats[1]}, ")
    print(f"Melhor Fitness: {test_stats[2]}, ")
    print(f"Pior Fitness: {test_stats[3]},")

    # Caminho da pasta onde o CSV será salvo
    output_folder = 'results/var_k_tour'

    # Garante que a pasta existe, cria caso contrário
    os.makedirs(output_folder, exist_ok=True)

    # Caminho completo do arquivo com a pasta incluída
    file_path = os.path.join(output_folder, f'test_stats_k_tour{k_tour}.csv')

    # Salvando todas as estatísticas em um arquivo CSV ao final do loop
    stats = []
    stats.append(test_stats)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Fitness Média', 'Fitness STD', 'Melhor Fitness', 'Pior Fitness'])  # Cabeçalhos
        writer.writerows(stats)

    print("Estatísticas de Teste salvas!\n")