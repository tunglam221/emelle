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
		for node in graph[i-1]:
			if x[i-2] not in self.emis:
				emis = self.emis[node.state]
			else:
				emis = self.emis[x[i-2]][node.state]
			score = node.score + log(self.tran[node.state][j]) + log(emis)
			if max_score < score:
				max_score = score
				parent = node
		return (max_score, parent)

	def decode(self, sentence):
		x = sentence.observation
		n = len(x)
		t = self.number_of_states
		graph = []

		# set node(0,0)
		graph.append([])
		graph[0].append(Node(0, None, 0))

		# time step 1
		graph.append([])
		for j in range(1, t-1):
			graph[1].append(Node(log(self.tran[0][j]), graph[0][0], j))

		for i in range(2, n+1):	#step i
			graph.append([])
			for j in range(1, t-1):
				_max = self.max_node(graph, i, j, x)
				graph[i].append(Node(_max[0], _max[1], j))

		# time step n+1
		graph.append([])
		_max = self.max_node(graph, n+1, t-1, x)
		graph[n+1].append(Node(_max[0], _max[1], t-1))

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

# tran = [[0, 0.5, 0, 0.5, 0],
# 		[0, 0, 0.4, 0.4, 0.2],
# 		[0, 0.2, 0, 0.2, 0.6],
# 		[0, 0.4, 0.6, 0, 0],
# 		[0, 0, 0, 0, 0]]

# emis = {'a': [0, 0.4, 0.4, 0.2, 0],
# 		'b': [0, 0.6, 0, 0.6, 0],
# 		'c': [0, 0, 0.6, 0.2, 0],
# 		1: 0.1, 2: 0.1, 3: 0.1}

# v = Viterbi(tran, emis)
# print(v.decode("b b"))
