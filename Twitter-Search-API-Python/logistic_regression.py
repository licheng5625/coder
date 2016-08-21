# -*- coding: utf-8 -*-
from numpy import genfromtxt
import numpy as np
import json
import matplotlib.pyplot as ma
#s=LR()
class LR(object):
	def __init__(self):
		self.trainX = None
		self.trainY = None
		self.testX = None
		self.testY = None
		self.theta = None
		self.trainRate=[]
		
		print("running.........")
		#self.loadTrainData()
        #	self.loadTestData()
        #	self.computeModelSGD()
		#self.testTheData()
		self.cest()
	
		
	def loadTrainData(self):
		listofrumor=[]
		listofnews=[]
		self.trainY=[]
		self.trainX=[]
		self.testX=[]
		self.testY=[]
		with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/data-nomal-single.txt', mode='r') as writer:
			for line in writer:
				JSON=json.loads(line)
				listofrumor.append(JSON)

		with open('/Users/licheng5625/PythonCode/masterarbeit/data/webpagefortwitter/Tweet_JSON/data-nomal-single2.txt', mode='r') as writer:
			for line in writer:
				JSON=json.loads(line)
				listofnews.append(JSON)
		for i in range (0,30000):#len(listofnews)-5):
			self.trainX.append(listofrumor[i][:-1])
			self.trainY.append(1)

		for i in range (0,30000):#len(listofnews)-5):
			self.trainX.append(listofnews[i][:-1])
			self.trainY.append(-1)

		for i in range (len(listofnews)-100,len(listofnews)):
			temp=[]
			temp=temp+listofrumor[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
			self.testX.append(temp)
			self.testY.append(1)
		for i in range (len(listofnews)-100,len(listofnews)):
			temp=[]
			temp=temp+listofnews[i][:-1]#[indexoffeaturelow:indexoffeaturelow+1]
			self.testX.append(temp)
			self.testY.append(-1)
		self.trainY=np.array(self.trainY)
		self.trainX=np.array(self.trainX)
		self.testX=np.array(self.testX)
		self.testY=np.array(self.testY)
	def loadTestData(self):
		self.testX, self.testY = self.loadXY("data-processed/test-processed.txt",0)      #Achtung!  Change your path here!!
	def loadXY(self, datafile,train):
		data = genfromtxt(datafile, delimiter='	')
		X = data[:,1:]
		Y = data[:,0]
		if train == 1:
    		  print("loading data done. Loaded %d training examples"%data.shape[0])
		else:
		  print("loading data done. Loaded %d testing examples"%data.shape[0])
		return X,Y
	def Evaluate(self):
				 NumOfGernerations=100
				 numofgroupe=8
				 mutationrate=0.1
				 i=0
				 groupe=self.initGernerations(numofgroupe)
				 (m,n)=groupe.shape
				 while (i!=NumOfGernerations):
				       chanceofsex=self.testThefitness(self.trainY,self.trainX,groupe)

	def initGernerations(self,Num):
		Groupe=np.array(self.theta,Num)
		size=Groupe.shape
		subGroupe1=Groupe[:,:size[0]/2]
		subGroupe2=Groupe[:,size[0]/2:]
		return Groupe

	def computeModelSGD(self):
		#m training examples (n-dimensional) 
		firstlrate = 0.9
		lrate = 0.5
		
		(m, n) = self.trainX.shape
		#initialize theta
		sigma = 0.1
		mu = 0
		#initialization of theta with random values
		theta = sigma * np.random.randn(n) + mu
		#going over training data (epochs)
		epochs=m
		X=[]
		NumofError=[]
		theta = sigma * np.random.randn(n) + mu
		print(m)
		print(n)
		for i in range(0, epochs):
				#the training example
				x = self.trainX[i]
				#the true label
				y = self.trainY[i]
				#the prediction
				hypothesis = np.dot(theta, x)
				print(hypothesis)

				sigmoid = 1 / (1 + np.exp(-hypothesis))
				print(sigmoid)
				theta += lrate * (y - sigmoid) * x
				self.theta = theta
				#print(theta)
		print("finish the training with learning rate %.3f and %d times training!"%(lrate, epochs))
        # NumofError.append(self.testTheData())
        #  X.append(epochs/float(m))
        #  ma.plot(X, NumofError, label='$Lrate= %.4f$'%lrate, linewidth=1.0, linestyle="-")
				       #print("2222")
				       #  ma.title(r"Logistic_Regression with diffrent lerning rate ")
				       #  ma.grid()
				       #  ma.xlabel("Train rate")
				       #   ma.ylabel("Error percent")
				       #   ma.legend()
				       #   ma.yticks([ 0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55])
				       #   ma.savefig(r"Logistic_Regression with diffrent lerning rate.jpg")
				       #    ma.show()
		return theta
	def cest(self):
		m=np.array(([4,3,2,1],[4,3,2,1],[4,3,2,1],[4,3,2,1]))
		n=m[:,0:2]
		l=m[:,2:]
		print (n)
		print(l)
		return 1
	def testThefitness(self,resultset,testset,Groupe):
    
		(m, n) = testset.shape
		size=Groupe.shape
		sum=0
		chanceofsex=np.zeros_like(Groupe)
		for i in range(0,size[0]):
			num=0
			for j in range(0,m):
				x = testset[j]
				hypothesis = np.dot(Groupe[i], x)
				result = 1 / (1 + np.exp(-hypothesis))
				y = self.testY[i]
				if result<0.5:
				   result=0
				else:
				   result=1
				if y == result:
					   num = num + 1
				chanceofsex[i]=num
				sum=num+sum
				print ("%d fitness is %.2f"%(i,float(num)/sum))
				for i in range(0,size[0]):
				    chanceofsex[i]=chanceofsex[i]/sum
				    if i!=0 :
				        chanceofsex[i]=chanceofsex[i-1]+chanceofsex[i]
		return chanceofsex

	def testTheData(self):
		num = 0
		(m, n) = self.testX.shape
		for i in range(0, m):
			x = self.testX[i]
			hypothesis = np.dot(self.theta, x)
			result = 1 / (1 + np.exp(-hypothesis))
						   #print(result)
			y = self.testY[i]
			print(result)
			if result<0.5:
					result=-1
			else:
					result=1
			#print(y)
			if y != result:
			   num = num + 1
		print("finish the testing with %0.2f percent Errors!"%(float(num)/m*100))
		return float(num)/m


lr=LR()
lr.loadTrainData()
lr.computeModelSGD()
lr.testTheData()