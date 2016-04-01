import random 
import math
import matplotlib.pyplot as plt
import json

class BloomFilter:

	def __init__(self,seed,n,k):
		random.seed(seed)
		self.rand=random.randint(0,n)
		self.n=n 
		self.filter=[0]*n
		self.k=k

	def reseed(self,seed):
		random.seed(seed)

	def choose_digits(self,datum):		
		random.seed(datum * self.rand)
		output=[]
		for i in xrange(int(self.k)):
			output.append(random.randint(0,self.n-1))
		return output

	def hashInput(self,input):
		digits=self.choose_digits(input)
		for digit in digits:
			#no_of_digits=n-(k*digits) if (i==k) else digits
			self.filter[digit] = 1
		return self.filter

	#def add_to_bloom(self,hashout):
		#self.filter= [(1 if (x ==1 or y==1) else 0 )for x, y in zip(self.filter, hashout)]

	def test_filter(self,test_number):
		digits=self.choose_digits(test_number)
		for digit in digits:
			if(not self.filter[digit] == 1):
				return False
		return True

def main():
	seed=123

	start_n=100
	end_n=10000

	start_m =100
	end_m= 2000

	step=50
	N = int(math.pow(2,20))-1

	collisions= [[0.0 for x in range(0,end_n-start_n,step)] for x in range(0,end_m-start_m,step)] 
	k=1

	for n in range(start_n,end_n,step): #table 
		print n
		for m in range(start_m,end_m,step): # number of entries being inserted
			c= n / m
			k = int(math.ceil(c * 0.69314718056)) #ln 2
			#print "K: %d"% k
			bloom_filter=BloomFilter(seed,n,k)
			values_to_insert=random.sample(range(0, N), m)
			for v in values_to_insert:
				bloom_filter.hashInput(v)

			#test all the numbers
			for t in range(0,N):
				if(bloom_filter.test_filter(t)):
					collisions[(m-start_m)/step][(n-start_n)/step]+= 1.0

			collisions[(m-start_m)/step][(n-start_n)/step]/= float(N)
			collisions[(m-start_m)/step][(n-start_n)/step ]*= float(100)
		print "Collisions %f" % (collisions[(m-start_m)/step][(n-start_n)/step ])
	save_file('data.json',collisions)
	plot(range(start_n,end_n,step),collisions[0])

def save_file(file_name,data):
	with open(file_name, 'w') as outfile:
   		json.dump(data, outfile)

def plot(x,y):
	plt.xlabel('n')
	plt.plot(x, y,'r--')
	plt.show()

main()