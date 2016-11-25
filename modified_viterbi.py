from heapq import nlargest
from viterbi import log
from state_num_dictionary import *

class PathNode:
	def __init__(self, score, parent, state):
		self.score = score
		self.parent = parent
		self.state = state
		
	def __repr__(self):
		if self.parent:
			return str(self.parent.state)
		else:
			return str(None)

class ModifiedViterbi:
	def __init__(self, tran, emis):
		self.tran = tran
		self.emis = emis

	def max_k_nodes(self, graph, step, state, x, k):
		scores = []
		if step > len(x): # STOP
			emis = 1
		elif x[step-1] not in self.emis:
			emis = self.emis[state]
		else:
			emis = self.emis[x[step-1]][state]

		# create a list of all possible scores
		for state_node in graph[step-1]:
			tran = self.tran[state_node[0].state][state]
			scores += map(lambda x: x.score + log(tran*emis) , state_node)

		# find the k best scores
		klargest = nlargest(k, scores)
		if k > len(klargest):
			k = len(klargest)

		# if a score is in the k best scores, note the parent node
		parents = [None]*k
		for state_node in graph[step-1]:
			tran = self.tran[state_node[0].state][state]
			for path_node in state_node:
				score = path_node.score+ log(tran*emis)
				if score in klargest:
					idx = klargest.index(score)
					while parents[idx]:
						if idx>=k-1:
							break
						idx+=1
					parents[idx] = path_node
		max_k = []
		for i in range(k):
			max_k.append(PathNode(klargest[i], parents[i], state))
		return max_k

	def decode(self, sentence, k):
		x = sentence.observation
		n = len(x)
		t = len(self.tran)
		graph = []

		# step 0
		graph.append([]) 	# step
		graph[0].append([]) # state node
		graph[0][0].append(PathNode(0, None, 0))

		# step i - recursive step
		for i in range(1, n+1): 
			graph.append([])
			for j in range(1, t-1):
				graph[i].append(self.max_k_nodes(graph, i, j, x, k))

		# step n+1
		graph.append([])
		graph[n+1].append(self.max_k_nodes(graph, n+1, t-1, x, k))
				
		for i in range(k):
			next = graph[n+1][0][i]
			path = []
			sentence.state.append([])
			for j in range(n+1, 1, -1):
				path.insert(0, next.parent.state)
				next = next.parent
			for p in path:
				sentence.state[i].append(num2state[p])


# tran = [[0, 0.5, 0, 0.5, 0],
# 		[0, 0, 0.4, 0.4, 0.2],
# 		[0, 0.2, 0, 0.2, 0.6],
# 		[0, 0.4, 0.6, 0, 0],
# 		[0, 0, 0, 0, 0]]

# emis = {'a': [0, 0.4, 0.4, 0.2, 0],
# 		'b': [0, 0.6, 0, 0.6, 0],
# 		'c': [0, 0, 0.6, 0.2, 0],
# 		1: 0.1, 2: 0.1, 3: 0.1}

# v = ModifiedViterbi(tran, emis)
# v.decode("b a", 2)
