import math
from state_num_dictionary import *

class Node:
	def __init__(self, score, parent, state):
		self.score = score
		self.parent = parent
		self.state = state

class Viterbi:
	def __init__(self, tran, emis, entity_emis):
		self.tran = tran
		self.emis = emis
		self.entity_emis = entity_emis
		self.number_of_states = len(tran)

	def max_node(self, graph, i, j, x, pretag, entity=''):
		max_score = -float('inf')
		parent = None
		if i > len(x):  # STOP state
			emis = 1
		elif pretag == 'O' and j!=1:
			emis = 0
		elif pretag == 'B':
			if j not in [2, 3, 4]:
				emis = 0
			else:
				emis = self.entity_emis[entity][j-2]
		elif pretag == 'I':
			if j not in [5, 6, 7]:
				emis = 0
			else:
				parent = graph[i-1][j-3]
				return Node(parent.score, parent, j)
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
		entities = sentence.findEntity(self.entity_emis)
		n = len(x)
		t = self.number_of_states
		graph = []

		# set node(0,0)
		graph.append([])
		graph[0].append(Node(0, None, 0))

		for i in range(1, n+1): #step i
			graph.append([])
			if entities[i-1]=='B':
				e = x[i-1]
				if i < len(entities):
					j=i
					while entities[j]=='I':
						e = e + ' ' + x[j]
						j+=1
						if j>= len(entities):
							break

				for j in range(1, t-1):
					graph[i].append(self.max_node(graph, i, j, x, 'B', e))
			else:
				for j in range(1, t-1):
					graph[i].append(self.max_node(graph, i, j, x, entities[i-1]))

		# step n+1
		graph.append([])
		graph[n+1].append(self.max_node(graph, n+1, t-1, x, 'X'))

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
