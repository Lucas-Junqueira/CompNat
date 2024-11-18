from gptree import GPTree
from symb_reg import fitness
from symb_reg import symbolic_regression
import random
import pandas as pd
import numpy as np
import os
import csv

# Conseguindo Dados
data_train = pd.read_csv('/home/lucasjunq/Desktop/CompNat/data/wineRed-train.csv')
data_train = data_train.iloc[:100]
data_test = pd.read_csv('/home/lucasjunq/Desktop/CompNat/data/wineRed-test.csv')
data_test = data_test.iloc[100:150]
X_train = data_train.iloc[:, :-1]
Y_train = data_train.iloc[:,-1]
Y_train = Y_train - 1
labels = Y_train.unique()
X_test = data_test.iloc[:, :-1]
Y_test = data_test.iloc[:,-1]
Y_test = Y_test - 1

variables = X_train.columns

# Definindo Parâmetros
operators = ['+','-','*','/','and','or','xor'] # Operadores
tam_pop = 100 # Tamanho da população inicial
n_ger = 50 # Números de gerações
p_mut = 0.6 # Probabilidade de mutação
p_cross = 0.3 # Probabilidade de CrossOver
k_tour = 2 # Número K para o torneio
n_elite = 2 # Número de elitistas
tam_max_ind = 7 # Tamanho maximo do indivíduo

# Treino / Teste variando tamanho das gerações
for i in range(1):

    # Definindo semente aleatória
    random.seed(42)

    print(f"Teste de numero {i}.\n")

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
    output_folder = 'results/wineRed'

    # Garante que a pasta existe, cria caso contrário
    os.makedirs(output_folder, exist_ok=True)

    # Caminho completo do arquivo com a pasta incluída
    file_path = os.path.join(output_folder, f'test_stats_wineRed.csv')

    # Salvando todas as estatísticas em um arquivo CSV ao final do loop
    stats = []
    stats.append(test_stats)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Fitness Média', 'Fitness STD', 'Melhor Fitness', 'Pior Fitness'])  # Cabeçalhos
        writer.writerows(stats)

    print("Estatísticas de Teste salvas!\n")