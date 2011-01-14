# pqueue implemented as heap
# items must have the item.value filled 

class container:
	def __init(self):
		pass
class heap:
	def __init__(self):
		self.__items = [None]
		self.__items_len = 0

	def isempty(self):
		return self.__items_len==0;

	def min(self):
		if self.__items_len == 0:
			raise IndexError("pop from an empty heap")
		return self.__items[1];

	def append(self,new):
		# just not to be always checking if reached the first element
		self.__items[0]=new
		self.__items_len +=1
		hole = self.__items_len;
		self.__items.append(None)
		# percolate up
		while new.value < self.__items[hole/2].value:
			self.__items[hole] = self.__items[hole/2]
			hole /=2
		self.__items[hole] = new

	def pop(self):
		if self.__items_len == 0:
			raise IndexError("pop from an empty heap")
		min = self.__items[1]
		self.__items[1] = self.__items[self.__items_len]
		self.__percolate_down(1)
		self.__items_len -=1
		return min

	def importlist(self,elements):
		self.__items = [None]
		self.__items_len = 0
		for element in elements:
			self.__items.append(element)
			self.__items_len +=1
		for i in range(self.__items_len/2,0,-1):
			self.__percolate_down(i)

	def __percolate_down(self,hole):
		tmp = self.__items[hole]
		
		while hole*2 <= self.__items_len:
			child = hole*2
			if (child != self.__items_len and
					 self.__items[child+1].value < self.__items[child].value):
				child+=1
			if self.__items[child].value<tmp.value:
				self.__items[hole] = self.__items[child]
			else:
				break
			hole = child
		
		self.__items[hole]=tmp
	
#values = [10,45,12,9,8,7,4,5,1,2,3]
#keys = ['A','B','C','D','E','F','G','H','I','J','K']

#pq = heap()
#objs=[]
#for k in range(len(keys)):
#	obj = container()
#	obj.value = values[k]
#	obj.key = keys[k]
#	objs.append(obj)
#	pq.append(obj)

#pq.importlist(objs)
#print pq.min().key , pq.pop().value
#print pq.min().key , pq.pop().value
