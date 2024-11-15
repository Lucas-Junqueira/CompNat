import random

random.seed(42)

class Node:
    """Esta classe modela os nódulos de uma árvore para a GP"""
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
    
    def evaluate(self, variables):
        """Avalia o nódulo de uma árvore recursivamente"""
        if self.left is None and self.right is None:
            if isinstance(self.value, str) and self.value in variables:
                return variables[self.value] #Nó é variável
            return float(self.value) #Nó é constante
        #Nó é operador
        left_value = self.left.evaluate(variables)
        right_value = self.right.evaluate(variables)
        return self.apply_operator(left_value,right_value)
    
    def apply_operator(self, left, right):
        """Aplica o operador"""
        if self.value == '+':
            return left + right
        elif self.value == '-':
            return left - right
        elif self.value == '*':
            return left * right
        elif self.value == '/':
            return left / right if right!=0 else float(0) #Evita divisão por zero
        elif self.value == 'and':
            left_int = int(left)
            right_int = int(right)
            return float(left_int & right_int)
        elif self.value == 'or':
            left_int = int(left)
            right_int = int(right)
            return float(left_int | right_int)
        elif self.value == 'xor':
            left_int = int(left)
            right_int = int(right)
            return float(left_int ^ right_int)
        else:
            raise ValueError(f"Operador desconhecido: {self.value}")
    
    def __str__(self):
        """Representa a árvore como uma expressão em notação infixa."""
        if self.left and self.right:
            return f'({self.left} {self.value} {self.right})'
        return str(self.value)
    
    def print_tree(self, variables=None, level=0):
        """Imprime a árvore de forma hierárquica, substituindo variáveis pelos valores do dicionário."""
        if self.right is not None:
            self.right.print_tree(variables, level + 1)
        
        # Imprime o valor ou o valor correspondente do dicionário
        if variables and self.value in variables:
            print("    " * level + str(variables[self.value]))
        else:
            print("    " * level + str(self.value))
        
        if self.left is not None:
            self.left.print_tree(variables, level + 1)
    
    def mutate(self):
        self.value

class GPTree:
    """Classe que representa um programa de programação genética baseado em árvores."""
    def __init__(self, depth, variables, operators, method='full', fitness=0):
        self.variables = variables
        self.operators = operators
        self.method = method
        self.fitness = fitness
        self.root = self.create_tree(depth)

    def __gt__(self, other):
        """Define o operador > (maior que) com base no atributo 'fitness'."""
        return self.fitness > other.fitness

    def __lt__(self, other):
        """Define o operador < (menor que) com base no atributo 'fitness'."""
        return self.fitness < other.fitness

    def __eq__(self, other):
        """Define o operador == (igual a) com base no atributo 'fitness'."""
        return self.fitness == other.fitness
    
    def __hash__(self):
        return hash((self.fitness))  # substitua com os atributos que definem exclusividade

    def create_tree(self, depth):
        if self.method == 'grow':
            return self.grow_method(depth)
        elif self.method == 'full':
            return self.full_method(depth)
        else:
            raise ValueError("Escolha entre os métodos 'grow' e 'full'.")
    
    def full_method(self, depth):
        """Cria um indivíduo com o método full"""
        if depth<0:
            raise ValueError("Depth menor que zero.")

        #Cria uma folha
        if depth==0:
            variable = random.choice(self.variables)
            return Node(variable)
        
        #Cria node operador
        operator = random.choice(self.operators)
        left_child = self.full_method(depth-1)
        right_child = self.full_method(depth-1)
        return Node(operator,left_child,right_child)
    
    def grow_method(self, depth):
        """Cria um indivíduo com o método full"""
        if depth<0:
            raise ValueError("Depth menor que zero")
        
        #Cria uma folha
        if depth==0 or random.random() < 0.4:
            variable = random.choice(self.variables)
            return Node(variable)

        #Cria node operator
        operator = random.choice(self.operators)
        left_child = self.grow_method(depth-1)
        right_child = self.grow_method(depth-1)
        return Node(operator,left_child,right_child)
    
    def evaluate(self, variables):
        """Faz avaliação da expressão que a árvore representa"""
        return self.root.evaluate(variables)
    
    def __str__(self):
        """Representa a árvore como uma expressão em notação infixa."""
        return str(self.root)

    def print_tree(self, variables):
        self.root.print_tree(variables=variables)
    
    def mutation_aux(self, current_node, mutation):
        """Função recursiva para realizar mutação"""
        if mutation[0] == True:
            return
        # 30% da mutação ocorrer neste nódulo
        elif random.random() < 0.2:
            #Caso folha
            if current_node.left is None and current_node.right is None:
                current_node.value = random.choice(self.variables)
                mutation[0] = True
            
            else:
                current_node.value = random.choice(self.operators)
                mutation[0] = True
        
        # Mutação não ocorre neste nódulo
        elif current_node.left is not None:
            if random.random() < 0.5:
                self.mutation_aux(current_node.left,mutation)
                self.mutation_aux(current_node.right,mutation)
            else:
                self.mutation_aux(current_node.right,mutation)
                self.mutation_aux(current_node.left,mutation)
    
    def mutation(self):
        """Função que realiza a mutação na árvore"""
        mutation = [False]
        while not mutation[0]:
            self.mutation_aux(self.root,mutation)
    
    def get_random_node_with_parent(self, current_node=None, parent=None, level=1):
        """Função recursiva que retorna um nó aleatório, seu pai, a posição (esquerda ou direita) e o nível."""
        if current_node is None:
            current_node = self.root

        # Lista de possíveis nós (nó atual e nós dos filhos)
        possible_nodes = [(current_node, parent, 'root', level)]
        
        # Adiciona nós dos filhos esquerdo e direito, se existirem
        if current_node.left:
            possible_nodes.append((current_node.left, current_node, 'left', level + 1))
            possible_nodes.extend(self.get_all_nodes_with_parent(current_node.left, current_node, level + 1))
        if current_node.right:
            possible_nodes.append((current_node.right, current_node, 'right', level + 1))
            possible_nodes.extend(self.get_all_nodes_with_parent(current_node.right, current_node, level + 1))
        
        # Seleciona um nó aleatório da lista de possíveis
        selected_node, selected_parent, position, selected_level = random.choice(possible_nodes)
        return selected_node, selected_parent, position, selected_level

    def get_all_nodes_with_parent(self, current_node, parent, level):
        """Função auxiliar para obter todos os nós com seus pais e níveis."""
        nodes_with_parent = [(current_node, parent, 'root' if parent is None else ('left' if parent.left == current_node else 'right'), level)]
        
        # Recorre para o filho da esquerda
        if current_node.left:
            nodes_with_parent.extend(self.get_all_nodes_with_parent(current_node.left, current_node, level + 1))
        # Recorre para o filho da direita
        if current_node.right:
            nodes_with_parent.extend(self.get_all_nodes_with_parent(current_node.right, current_node, level + 1))
        
        return nodes_with_parent
    
    def escolher_node_nivel(self, nivel_especifico):
        # Função auxiliar para coletar nós em um nível específico com informações do pai e posição
        def coletar_nos_nivel(node, nivel_atual, nivel_alvo, nos_do_nivel, pai=None, posicao=None):
            if node is None:
                return
            if nivel_atual == nivel_alvo:
                nos_do_nivel.append((node, pai, posicao))
            else:
                # Procura no filho esquerdo
                coletar_nos_nivel(node.left, nivel_atual + 1, nivel_alvo, nos_do_nivel, node, 'left')
                # Procura no filho direito
                coletar_nos_nivel(node.right, nivel_atual + 1, nivel_alvo, nos_do_nivel, node, 'right')

        # Tenta coletar nós a partir do nível especificado, retrocedendo se necessário
        nivel_atual = nivel_especifico
        while nivel_atual >= 1:
            nos_do_nivel = []
            coletar_nos_nivel(self.root, 1, nivel_atual, nos_do_nivel)
            
            # Se encontrou nós no nível atual, escolhe um aleatório
            if nos_do_nivel:
                node, pai, posicao = random.choice(nos_do_nivel)
                # Verifica se o nó escolhido é a raiz
                if node == self.root:
                    posicao = "root"
                return node, pai, posicao

            # Retrocede para o nível anterior
            nivel_atual -= 1

        # Se não encontrou nenhum nó, retorna None
        print("Nenhum nó encontrado na árvore.")
        return None, None, None