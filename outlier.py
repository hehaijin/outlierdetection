import pandas as pd
import numpy as np






#check z-score
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
	
	
#
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
				
	
	


#DBOutlierByFeature("F"+str(4),2,0.01 )

df0=pd.read_csv("data.csv",names=['class','F1','F2','F3','F4','F5','F6','F7','F8'])
df0["id"]=df0.index

dfs=[]
for i in range(1,5):
	df=df0.loc[ df0['class']==i]
	dfs.append(df)



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

for id in set(outlier):
	print(df0.loc[df0["id"]==id])




