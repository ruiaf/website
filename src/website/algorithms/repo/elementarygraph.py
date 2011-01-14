# Python rules graph algorithms because of dictionaries.
# adjency hashtable :)

edges = [('A',['G','B','F']),('B',['C','D','E']),('C',[]),\
		('D',[]),('E',['G']),('F',['E']),('G',[])]
visited = {}
graph = {}

def clear():
	for (node,con) in edges:
		visited[node]=False

for (node,con) in edges:
	visited[node]=False
	graph[node]=dict()

for (node,connections) in edges:
	for con in connections:
		graph[node][con]=True
		graph[con][node]=True

# Depth First Search 

def dfs_visit(node):
	visited[node]=True
	print node
	for nextnode in graph[node].keys():
		if not visited[nextnode]:
			dfs_visit(nextnode)

def depth_first_search():
	for node in visited.keys():
		if not visited[node]:
			dfs_visit(node)
	

# Breath First Search

queue = []

def bfs_visit(node):
	queue.append(node)
	while len(queue)>0:
		curnode=queue.pop(0)
		print curnode
		visited[curnode]=True
		for con in graph[curnode].keys():
			if visited[con]==False:
				queue.append(con)
				visited[con]="in queue"
		

def breath_first_search():
	for node in visited.keys():
		if not visited[node]==True:
			bfs_visit(node)
	
	

print "DFS"
depth_first_search()
clear()
print "BFS"
breath_first_search()

