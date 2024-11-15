from gptree import GPTree
from symb_reg import crossover
import random

# Definindo semente aleatória
# random.seed(10)

# variables = ['A','B','C','D']
# operators = ['+','-','*','/']
# dictionary = {'A':5, 'B':4, 'C':3, 'D':2}
# max_depth = 4
# max_depth = max_depth-1

# Trees = []
# for i in range(2):
#     Trees.append(GPTree(max_depth,variables,operators,method='full'))
# print("Antes\n")
# print("Arvore 1: \n")
# Trees[0].print_tree(dictionary)
# print("Arvore 2: \n")
# Trees[1].print_tree(dictionary)
# crossover(Trees[0],Trees[1],variables,max_depth)
# print("\nDepois\n")
# print("Arvore 1: \n")
# Trees[0].print_tree(dictionary)
# print("Resultado: ", Trees[0].evaluate(dictionary))
# print("Arvore 2: \n")
# Trees[1].print_tree(dictionary)
# print("Resultado: ", Trees[1].evaluate(dictionary))

# for tree in Trees:
#     print("Expressão: \n")
#     tree.print_tree(dictionary)
#     #print("Resultado: ", tree.evaluate(dictionary))
#     print("\n")
#     tree.mutation()
#     print("Mutação: \n")
#     tree.print_tree(dictionary)

from collections import Counter

# Lista com elementos
lista = [1, 2, 2, 3, 3, 3, 1]

# Contando as ocorrências de cada elemento na lista
contador = Counter(lista)

# Calculando a quantidade de indivíduos repetidos
# Um "indivíduo repetido" é aquele que aparece mais de uma vez na lista
repetidos = sum(1 for count in contador.values() if count > 1)

print(f"Quantidade de indivíduos repetidos: {repetidos}")
