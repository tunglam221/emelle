import math
from state_num_dictionary import *

class Node:
        def __init__(self, score, parent, state):
                self.score = score
                self.parent = parent
                self.state = state

class Viterbi:
        def __init__(self, tran, emis):
                self.tran = tran
                self.emis = emis
                self.number_of_states = len(tran)

        def max_node(self, graph, i, j, x):
                max_score = -float('inf')
                parent = None
                if i > len(x):  # STOP state
                        emis = 1
                elif x[i-1] not in self.emis:
                        emis = self.emis[j]
                else:
                        emis = self.emis[x[i-1]][j]
                for node in graph[i-1]:
                        score = node.score + log(self.tran[node.state][j]) + log(emis)
                        if max_score <= score:
                                max_score = score
                                parent = node
                return Node(max_score, parent, j)

        def decode(self, sentence):
                x = sentence.observation
                n = len(x)
                t = self.number_of_states
                graph = []

                # set node(0,0)
                graph.append([])
                graph[0].append(Node(0, None, 0))

                for i in range(1, n+1): #step i
                        graph.append([])
                        for j in range(1, t-1):
                                graph[i].append(self.max_node(graph, i, j, x))

                # step n+1
                graph.append([])
                graph[n+1].append(self.max_node(graph, n+1, t-1, x))

                path = []
                next = graph[n+1][0]
                for i in range(n+1, 1, -1):
                        path.insert(0, next.parent.state)
                        next = next.parent

                for p in path:
                        sentence.state.append(num2state[p])

def log(a):
        if a==0:
                return -float('inf')
        else:
                return math.log(a)
