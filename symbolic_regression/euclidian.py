import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.cluster import v_measure_score

"""Realizando testes com a distancia euclidina para o algoritmo de cluster"""

# Coletando dados - Base Breast Cancer:
data_train = pd.read_csv('/home/lucasjunq/Desktop/CompNat/data/breast_cancer_coimbra_train.csv')
X_bcancer = data_train.drop(columns=['Classification'])
Y_bcancer = data_train['Classification']
Y_bcancer = Y_bcancer - 1
labels_bcancer = Y_bcancer.unique()

# Base # Coletando dados - Base Wine Red:
data_train = pd.read_csv('/home/lucasjunq/Desktop/CompNat/data/wineRed-train.csv')
data_train = data_train.iloc[:100]
data_test = pd.read_csv('/home/lucasjunq/Desktop/CompNat/data/wineRed-test.csv')
data_test = data_test.iloc[100:150]
X_train = data_train.iloc[:, :-1]
Y_train = data_train.iloc[:,-1]
Y_train = Y_train - 1
labels_wine = Y_train.unique()
X_test = data_test.iloc[:, :-1]
Y_test = data_test.iloc[:,-1]
Y_test = Y_test - 1
X_wine = X_train
Y_wine = Y_train

print("Resultados dos testes:\n")

# Resultado para a Base Breast Cancer
clustering = AgglomerativeClustering(n_clusters=len(labels_bcancer),metric='euclidean',linkage='average')
clustering.fit(X_bcancer)
print("V Score para a base Breast Cancer:",v_measure_score(Y_bcancer,clustering.labels_))

# Resultado para a Base WineRed
clustering = AgglomerativeClustering(n_clusters=len(labels_wine),metric='euclidean',linkage='average')
clustering.fit(X_wine)
print("V Score para a base WineRed:",v_measure_score(Y_wine,clustering.labels_))