# Implementation of the Fast Map algorithm

import random as rand
import numpy as np
import matplotlib.pyplot as plt
import scipy

from Crypto.Random.random import randint

f =  open('dims.txt','r')
data = f.readlines()

dimensionsOuter  = []

for x in data:
    lis = x.rstrip().split(",")
    dimensionsInner = []
    for i in lis:
        iValue = float(i)
        dimensionsInner.append(iValue)        
    dimensionsOuter.append(dimensionsInner)

result = scipy.zeros((len(dimensionsOuter),2)) 
global columnNo
columnNo = -1

# Calculates the Euclidean distance between two Data points    
def dist(i, j):
    sum = 0
    point1 = dimensionsOuter[i]
    point2 = dimensionsOuter[j]
    for k in range(0,len(point1)):
        sum += (point1[k] - point2[k])**2
    return np.math.sqrt(sum)

distMatrixOuter = []
for i in range(0,len(dimensionsOuter)):
    lis = dimensionsOuter[i]
    distMatrixInner = []
    for j in range(0,len(dimensionsOuter)):
        distMatrixInner.append(dist(i,j))
    distMatrixOuter.append(distMatrixInner)
    
c = np.matrix(distMatrixOuter)

# Function to find the Data point with the maximum distance from the current object       
def findMaxDist(obj): 
    max = float('-inf') 
    maxIndex = None
    for i in range(0, len(dimensionsOuter[obj])):
        if obj != i:
            if distMatrixOuter[obj][i] > max:
                max = distMatrixOuter[obj][i]
                maxIndex = i
    return maxIndex
 
# Function to find the pivot Objects Oa and Ob        
def chooseDistantObjects():
    randomIndex = randint(0,99)
    x0 = randomIndex
    for i in range(0, len(dimensionsOuter)):
        Oa = findMaxDist(x0)
        Ob = findMaxDist(Oa)
    return(Oa,Ob)
 
# Distance function                    
def distance(point1, point2, k):
    if k == 0:
        return distMatrixOuter[point1][point2];
    # Old Distance ^ 2
    oldDistance = distance(point1, point2, k - 1)
    # (Xi - Xj) ^ 2
    interceptDifference = (result[point1][k] - result[point2][k]) ** 2
    return abs(oldDistance - interceptDifference)  
 
# Function to calculate the intercept        
def intercept(i,point1, point2, colNo):
    dix = distance(i, point1, colNo)
    diy = distance(i, point2, colNo)
    dxy = distance(point1, point2, colNo)
    return (dix + dxy - diy) / 2 * np.math.sqrt(dxy)    

# Fast Map algorithm    
def fastMap(k, columnNo):
    
    if k == 0:
        return
    else:
        columnNo += 1
    
    pivotX, pivotY = chooseDistantObjects() 
    
    if distance(pivotX, pivotY, columnNo) == 0:
        for i in range(0,len(dimensionsOuter)):
            result[i][columnNo] = 0;           
        return

    for i in range(0,len(dimensionsOuter)):
        result[i][columnNo] = intercept(i, pivotX, pivotY, columnNo)
        
    fastMap(k - 1, columnNo)

fastMap(2, columnNo)

# Display output
print "------------- Result ---------------"
print result

# Write to Output file
fw = open('FastMapOutput.txt','w')
fw.write("------------- Result ---------------\n")
for item in result:
    fw.write("%s\n" % item) 

fw.close()

# Display the result
for row in result:
    x = row[0]
    y = row[1]
    plt.scatter(x,y)

plt.ylabel('y')   
plt.xlabel('x')
plt.show()