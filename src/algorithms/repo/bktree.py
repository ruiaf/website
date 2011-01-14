def levenshtein_distance(s,t):
	d = dict()
	for i in range(len(s)+1):
		d[i,0] = i
	for j in range(len(t)+1):
		d[0,j] = j

	for i in range(1,len(s)+1):
		for j in range(1,len(t)+1):
			d[i,j] = min(
				d[i-1,j]+1,
				d[i,j-1]+1,
				d[i-1,j-1]+(s[i-1]!=t[j-1]))
	
	return d[len(s),len(t)]


class _bktree__node():
	def __init__(self,v):
		self.value = v
		self.children = dict()

class bktree():
	def __init__(self,distance_fn):
		self.dfn = distance_fn
		self.root = __node("")

	def insert(self,new_string):
		node = self.root
		while True:
			distance = self.dfn(node.value,new_string)
			if distance==0:
				return 0

			if node.children.has_key(distance):
				node = node.children[distance]
			else:
				node.children[distance] = __node(new_string)
				return distance

	def search(self,word,max_d):
		return self.__node_search(word,max_d,self.root)

	def __node_search(self,word,max_d,node):
		d = self.dfn(node.value,word)
		answer = []
		if d <= max_d:
			answer.append((node.value,d))
		for k in [k for k in node.children.keys() if abs(d-k)<=max_d]:
			answer.extend(self.__node_search(word,max_d,node.children[k]))
		return answer

t = bktree(levenshtein_distance)
print t.insert("cat")
print t.insert("dog")
print t.insert("happening")
print t.insert("happened")
print t.insert("today")
print t.insert("yesterday")
print t.insert("did you mean")

print t.search("erday",3)
print t.search("happens",5)
print t.search("did je men?",5)

