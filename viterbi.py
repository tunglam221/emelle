class Node:
	def __init__(self, score, parent, state):
		self.score = score
		self.parent = parent
		self.state = state

class Viterbi:
	def __init__(self, tran, emis):
		self.tran = tran
		self.emis = emis

	def max_node(self, graph, i, j, x):
		max_score = 0
		parent = None
		for node in graph[i-1]:
			if x[i-2] not in self.emis:
				emis = self.emis[node.state]
			else:
				emis = self.emis[x[i-2]][node.state]
			score = node.score*self.tran[node.state][j]*emis
			if max_score < score:
				max_score = score
				parent = node
		return (max_score, parent)


	def decode(self, sentence):
		x = sentence.split()
		n = len(x)
		t = len(self.tran)
		graph = []

		# set node(0,0)
		graph.append([])
		graph[0].append(Node(1, None, 0))

		# time step 1
		graph.append([])
		for j in range(1, t-1):
			graph[1].append(Node(self.tran[0][j], graph[0][0], j))

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

		return path

tran = [[0, 0.5, 0, 0.5, 0],
		[0, 0, 0.4, 0.4, 0.2],
		[0, 0.2, 0, 0.2, 0.6],
		[0, 0.4, 0.6, 0, 0],
		[0, 0, 0, 0, 0]]

emis = {'a': [0, 0.4, 0.4, 0.2, 0],
		'b': [0, 0.6, 0, 0.6, 0],
		'c': [0, 0, 0.6, 0.2, 0],
		1: 0.1, 2: 0.1, 3: 0.1}

# emis = {(1, 'a'): 0.4, (1, 'b'): 0.6, (1, 'c'): 0, (1): 0.1,
# 		(2, 'a'): 0.4, (2, 'b'): 0, (2, 'c'): 0.6, (2): 0.1,
# 		(3, 'a'): 0.2, (3, 'b'): 0.6, (3, 'c'): 0.2, (3): 0.1}

v = Viterbi(tran, emis)
print(v.decode("b d"))
