from heapq import nlargest
from viterbi import log

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

		# create a list of all possible scores
		for state_node in graph[step-1]:
			tran = self.tran[state_node[0].state][state]
			if x[step-2] not in self.emis:
				emis = self.emis[state_node[0].state]
			else:
				emis = self.emis[x[step-2]][state_node[0].state]
			scores += map(lambda x: x.score + log(tran*emis) , state_node)

		# find the k best scores
		klargest = nlargest(k, scores)
		if k > len(klargest):
			k = klargest

		# if a score is in the k best scores, note the parent node
		parents = [None]*k
		for state_node in graph[step-1]:
			tran = self.tran[state_node[0].state][state]
			if x[step-2] not in self.emis:
				emis = self.emis[state_node[0].state]
			else:
				emis = self.emis[x[step-2]][state_node[0].state]
			for path_node in state_node:
				score = path_node.score+ log(tran*emis)
				if score in klargest:
					idx = klargest.index(score)
					while parents[idx]:
						if idx>=k-1:
							break
						idx+=1
					parents[idx] = path_node
				#print(klargest)
		return (klargest, parents)

	def decode(self, sentence, k):
		x = sentence.split()
		n = len(x)
		t = len(self.tran)
		graph = []

		# set node(0,0)
		graph.append([]) 	# step
		graph[0].append([]) # state node
		graph[0][0].append(PathNode(0, None, 0))
				
		# step 1
		graph.append([])
		for j in range(1, t-1):
			graph[1].append([])
			graph[1][j-1].append(PathNode(log(self.tran[0][j]), graph[0][0][0], j))

		# step i - recursive step
		for i in range(2, n+1): 
			graph.append([])
			for j in range(1, t-1):
				graph[i].append([])
				max_k = self.max_k_nodes(graph, i, j, x, k)
				for a in range(len(max_k)):
					graph[i][j-1].append(PathNode(max_k[0][a], max_k[1][a], j))

		# step n+1
		graph.append([])
		max_k = self.max_k_nodes(graph, n+1, t-1, x, k)
		graph[n+1].append([])
		for a in range(k):
			graph[n+1][0].append(PathNode(max_k[0][a], max_k[1][a], t-1))
				
		paths = []
		for i in range(k):
			next = graph[n+1][0][i]
			path = []
			for j in range(n+1, 1, -1):
				path.insert(0, next.parent.state)
				next = next.parent
			paths.append(path)	
		return paths

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
# print(v.decode("a b", 2))
