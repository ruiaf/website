# A-star algorithm, A*

# pqueue.py, available in ruiaf.org
from pqueue import heap,container
from math import sqrt

#('city',[('city1','distancebytrain'),.....],(coordx,coordy))
# don't mind city positioning too much :)
edges = [('Lisbon',[('Madrid',4),('Paris',12)],(0,0)),
         ('Madrid',[('Athens',12),('Berlin',15)],(2,2)),
	 ('Athens',[('Moscow',2)],(8,10)),
         ('Paris',[('Berlin',5)],(5,5)),
	 ('Berlin',[('Budapest',8),('Warsaw',6)],(6,7)),
         ('Budapest',[('Moscow',8)],(5,10)),
	 ('Warsaw',[('Moscow',4)],(7,11)),
         ('Moscow',[],(8,11))]
node_list = {}
node_coord = {}
graph = {}

for (node,con,coord) in edges:
	node_list[node]=None
	node_coord[node]=coord
	graph[node]=dict()

for (node,connections,coord) in edges:
	for (con,weight) in connections:
		graph[node][con]=weight
		graph[con][node]=weight

# has to be a lower bownder for the distance
# we are using euclidean because the graph was made
# taking that into account
# if this heuristic returns 0, it's dykstra algorithm!
def heuristic(node1,node2):
	#return 0
	difx = node_coord[node1][0]-node_coord[node2][0]
	dify = node_coord[node1][0]-node_coord[node2][0]
	return sqrt(difx*difx+dify*dify)


def astar(startpoint,endpoint):
	pq = heap()
	node = container()
	node.value = 0
	node.distance = 0
	node.key = startpoint
	node.previous_node = None
	pq.append(node)

	while not pq.isempty():
		node = pq.pop()
		if node_list[node.key]!=None:
			#we have already checked this node, move along!
			#it could be possible to avoid this by cross-referencing
			#the nodes and the pqueue elements, updating the values there
			#then only a percolateup would be needed instead of
			#adding several times the same element to the pq
			continue
		node_list[node.key]=(node.previous_node,node.distance)

		if node.key==endpoint:
			break

		for child_node in graph[node.key].keys():
			child = container()
			child.key = child_node
			child.distance = graph[node.key][child_node]+node.distance
			child.value = child.distance+heuristic(child.key,endpoint)
			child.previous_node = node.key
			pq.append(child)

astar('Lisbon','Moscow')
for node in node_list.keys():
	print node, node_list[node]

