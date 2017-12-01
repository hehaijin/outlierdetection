import pandas as pd
import numpy as np
import math
from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import random


#check z-score
#this is to use z-score to find outlier. not used in report.
def getOutlierByFeature(df,feature):
	v=df[feature].values
	mean=np.mean(v)
	std=np.std(v)
	outlier=[]
	
	for i in range(len(v)):
		dev= v[i]-mean
		dev=dev/std
		if abs(dev) > 3:
			#print(df.iloc[i])
			outlier.append(i)
	return i
	
	
#distance based outlier detection for each class and feature
def DBOutlierByFeature(df,feature, r, pi):
	v=df[feature].values
	N=len(v)
	outlier=[]
	for i in range(N):
		count=0
		for j in range(N):
			if i != j:
				if abs(v[i]-v[j]) < r:
					count=count+1
				if count >= pi* N:
					break
		if count < pi*N:
			outlier.append(i)
	#print(outlier)
	return outlier			
				

def GloabalDBOutlier(data,r,pi):
	#data=df.as_matrix(columns=['F1','F2','F3','F4','F5','F6','F7','F8'])
	N=len(data)
	print(N)
	outlier=[]
	for i in range(N):
		if i%1000==0:
			print("working on data "+str(i)) 
		count=0
		temp=[]
		for j in range(N):
			if i != j:
				if distance(data[i],data[j]) < r:
					count=count+1
					temp.append(j)
				if count >= pi* N:
					break
		if count < pi*N:
			outlier.append(i)
			print("hit one outlier")
			print(i)
			print(temp)
	
	#print(outlier)
	return outlier		
	
	
def distance(a,b):
	if len(a)!= len(b):
		raise ValueError('input dimensions for calculating distance must be the same')
	N=len(a)
	l=0
	for i in range(N):
		l=l+ (a[i]-b[i])* (a[i]-b[i])
	l=math.sqrt(l)
	return l
	
	
#normalize data by each feature.	
def normalizeByFeature(dataarray):
	(h,w)=dataarray.shape

	#removeinfnan(dataarray)		
	result=np.zeros((h,w))
	ave=np.nanmean(dataarray,axis=0)  #ignore nan. hiphop 36 37 gives nan result
	var=np.nanvar(dataarray,axis=0)   #ignore nan 
	for i in range(h):
		for j in range(w):
			if var[j]!=0:
				result[i,j]= (dataarray[i,j]-ave[j])/var[j]
			else:
				result[i,j]= dataarray[i,j]-ave[j]
	return result
	
#distance based outlier function for each feature.
def outlier1():

	#DBOutlierByFeature("F"+str(4),2,0.01 )

	df0=pd.read_csv("data.csv",names=['class','F1','F2','F3','F4','F5','F6','F7','F8'])
	
	df0["id"]=df0.index


	#split data into different class
	dfs=[]
	for i in range(1,5):
		df=df0.loc[ df0['class']==i]
		dfs.append(df)

	#data=df0.as_matrix(columns=['F1','F2','F3','F4','F5','F6','F7','F8'])
	#get all the outlier ids
	
	outlier=[]
	for i in range(4):
		print("working on class "+str(i))
		for j in range(1,9):
			r=DBOutlierByFeature(dfs[i],"F"+str(j),10,0.0004 )   # 4 poinnts in 10 radius
			for o in r:
				id=(dfs[i].iloc[o])["id"]
				outlier.append(id)

	print("all outlier ids:")
	print(set(outlier))

	#print the outlier data
	resultdf= df0[df0["id"].isin(outlier)]
	resultdf.to_csv("DistanceOutlierUni.csv",index=False)
	
# global distance based outlier function
def outlier2():

	#DBOutlierByFeature("F"+str(4),2,0.01 )

	df0=pd.read_csv("data.csv",names=['class','F1','F2','F3','F4','F5','F6','F7','F8'])
	
	df0["id"]=df0.index

	data=df0.as_matrix(columns=['F1','F2','F3','F4','F5','F6','F7','F8'])
	data=normalizeByFeature(data)
	#split data into different class
	
	outlier=GloabalDBOutlier(data,0.0025, 0.0002)
	resultdf= df0[df0["id"].isin(outlier)]
	resultdf.to_csv("DistanceOutlierMulti.csv",index=False)



def clustering(data):
	
	cluster=AgglomerativeClustering(5, linkage='average' )
	cluster.fit(data)
	df=pd.DataFrame({"label":cluster.labels_})
	df.to_csv("result.csv",index=False)


def getMinFromMatrix(M):
	N=len(M)
	m=M[0][0]
	a=0
	b=0
	for i in range(N):
		for j in range(i+1,N):
			if M[i][j]<m:
				a=i
				b=j
	return (a,b)


#use hierarchical clustering to get class 5
def HCAverage(data):
	N=len(data)
	M=np.zeros((N,N))
	print("data size"+str(N))
	C=[]
	for i in range(N):
		C.append([(i,data[i])])
	
	for i in range(N):
		#print("data point "+str(i))
		for j in range(i+1,N):
			M[i,j]=distance(data[i],data[j])
			M[j,i]=M[i,j]
	print("distance Matrix generated")
	CM=M
	q=N
	print("group size "+str(q))
	while q>5:
		print(q)
		a,b=getMinFromMatrix(CM)
		Cb=C.pop(b)
		Ct=C[a]+Cb
		C[a]=Ct
		q=q-1
		CM2=np.zeros((q,q))
		for i in range(q):
			for j in range(i+1,q):
				if i < a and j < a:
					CM2[i][j]=CM[i][j]
				else: 
					Na=len(C[i])
					Nb=len(C[j])
					t=0
					for l in range(Na):
						for m in range(Nb):
							
							ia=C[i][l][0]
							ib=C[j][m][0]
							
							t=t+M[ia][ib]
					for l in range(Na):
						for m in range(l+1,Na):
							ia=C[i][l][0]
							ib=C[i][m][0]
							t=t+M[ia][ib]
					for l in range(Nb):
						for m in range(l+1,Nb):
							ia=C[j][l][0]
							ib=C[j][m][0]
							t=t+M[ia][ib]
					t=t/Na/Nb
					CM2[i][j]=t
		CM=CM2
	outliercount=N
	outliergroup=N			
	for i in range(5):
		if outliercount< len(C[i]):
			outliercount=len(C[i])
			outliergroup=i
		print(len(C[i]))						
	print("outlier group")
		
		
#main function		
def main():
	outlier1()
	outlier2()
	


def hierarchical():
	df0=pd.read_csv("data.csv",names=['class','F1','F2','F3','F4','F5','F6','F7','F8'])
	
	df0["id"]=df0.index

	data=df0.as_matrix(columns=['F1','F2','F3','F4','F5','F6','F7','F8'])
	data2=[]
	for i in range(len(data)):
		if random.random()<0.01:
			data2.append(data[i])
	data2.append(data[999])
	data3=np.asarray(data2)
	print("data generated")
	HCAverage(data3)

if __name__=='__main__':
	main()
