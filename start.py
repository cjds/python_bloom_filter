import random 
import math
import matplotlib.pyplot as plt
import json

class BloomFilter:

	def __init__(self,seed,n,k):
		random.seed(seed)
		self.random=random.randint(0,seed)
		self.n=n
		self.filter=[0]*n
		self.k=k

	def reseed(self):
		random.seed(seed)

	def hashInput(self,input):
		output=[]
		random.seed(input)
		current_filter=[0]*self.n
		for i in range(int(self.k)):
			#no_of_digits=n-(k*digits) if (i==k) else digits
			hashout=random.randint(0,self.n-1)
			current_filter[hashout] = 1
			
		return current_filter

	def add_to_bloom(self,hashout):
		self.filter= [(1 if (x ==1 or y==1) else 0 )for x, y in zip(self.filter, hashout)]

	def test_filter(self,test_number):
		for i,digit in enumerate(self.filter):
			if(test_number[i]==1 and not digit==1):
				return False
		return True


def main():
	seed=123

	start_n=5500
	end_n=6000

	start_m =1000
	end_m= 1200

	step=50
	N = int(math.pow(2,12))-1

	collisions= [[0 for x in range(0,end_n-start_n,step)] for x in range(0,end_m-start_m,step)] 

	k=1

	for n in range(start_n,end_n,step): #table size
		for m in range(start_m,end_m,step): # number of entries being inserted
			c= n / m
			k = int(math.ceil(c * 0.69314718056)) #ln 2
			bloom_filter=BloomFilter(seed,n,k)
			for b in xrange(0,m):
				v=random.randint(0,N) #choose randomly from the size of universe
				hashedv=bloom_filter.hashInput(v)
				while not bloom_filter.test_filter(hashedv):
					v=random.randint(0,N)
				bloom_filter.add_to_bloom(hashedv)

			#test all the numbers
			for t in range(0,N):
				if(bloom_filter.test_filter(bloom_filter.hashInput(t))):
					collisions[(m-start_m)/step-1][(n-start_n)/step]+= 1

			collisions[(m-start_m)/step-1][(n-start_n)/step]/= float(N)
			collisions[(m-start_m)/step-1][(n-start_n)/step ]*= float(100)
	plot(range(start_n,end_n,step),collisions[1])

def save_file(file_name,data):
	with open('data.json', 'w') as outfile:
   		json.dump(collisions, outfile)

def plot(x,y):
	plt.xlabel('n')
	plt.plot(x, y,'r--')
	plt.show()

main()