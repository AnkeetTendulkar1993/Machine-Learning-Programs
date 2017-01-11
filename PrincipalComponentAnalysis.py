# Implementation of Principal Component Analysis

import numpy as np
import matplotlib.pyplot as plt

f = open('dims.txt','r')  
data = f.readlines()

dimensionsOuter = []

for x in data:
    lis = x.rstrip().split(",")
    dimensionsInner = []
    for i in lis:
        temp = float(i)
        dimensionsInner.append(temp)       
    dimensionsOuter.append(dimensionsInner)

originalMatrix = np.matrix(dimensionsOuter)
        
temp = []
   
d1 = originalMatrix.sum(axis=0, dtype='float')
d = d1 / float(len(dimensionsOuter))

covMatrixOuter = []
for i in range(0,len(dimensionsOuter)):
    covMatrixInner = []
    for j in range(0,len(dimensionsOuter[0])):
        s = originalMatrix.item(i,j) - d.item(j)       
        covMatrixInner.append(originalMatrix.item(i,j) - d.item(j))
    covMatrixOuter.append(covMatrixInner)
 
partialCovarianceMatrix = np.matrix(covMatrixOuter)            
covTemp = np.matrix(partialCovarianceMatrix)
covarianceMatrix = np.divide(np.dot(covTemp.T,covTemp),(len(dimensionsOuter) - 1))

print "------------- The Covariance matrix ----------------"
print covarianceMatrix

eigenValue, eigenVector = np.linalg.eig(covarianceMatrix)

print "----------------- Eigen Vectors --------------- \n", eigenVector
print "----------------- Eigen Values --------------- \n", eigenValue

# Sorting the Eigen vectors based on Eigen values
idVal = eigenValue.argsort()[::-1]   
eigenValuesSorted = eigenValue[idVal]
eigenVectorsSorted = eigenVector[:,idVal]
   
m = eigenVectorsSorted.tolist()
temp = []
temp.append(m[0])
temp.append(m[1])

# Displaying the top k rows
print "----------- The k x n matrix ----------- "
topKRows = np.matrix(temp)
print topKRows

# The resulting matrix
result = np.dot(originalMatrix, topKRows.T)
print "----------------- Result -----------------"
print result

# Storing the data in output file
fw = open('PrincipalComponentAnalysisOutput.txt', 'w')
fw.write("------------- The Covariance matrix ----------------\n")
for row in covarianceMatrix:
    outer = row.tolist()
    for col in outer:
        fw.write("%s " % col)
    fw.write("\n")

fw.write("----------------- Eigen Vectors --------------- \n")
for row in eigenVector:
    outer = row.tolist()
    for col in outer:
        fw.write("%s " % col)
    fw.write("\n")

fw.write("----------------- Eigen Values --------------- \n")
for x in eigenValue:
    fw.write("%s " %x)
    

fw.write("\n------------- Result Matrix ----------------\n")
for row in result:
    outer = row
    for col in outer:
        fw.write("%s " % col)
    fw.write("\n")

fw.close()

# Displaying the result data 
resultList = result.tolist()
for row in resultList:
    x = row[0]
    y = row[1]
    plt.scatter(x,y)

plt.ylabel('y')  
plt.xlabel('x') 
plt.show()