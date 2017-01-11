# Implementation of Support Vector Machines

from sklearn import svm

import numpy as np
import matplotlib.pyplot as plt

f = open('nnsvm-data.txt','r')
input = f.readlines()

dataPointsOuter = []
originalDataOuter = []
target = []

# Reading all the datapoints
for row in input:
    lis = row.rstrip().split(" ")
    originalDataInner = []
    dataPointsInner = []
    for i in range(0,len(lis) - 1):
        val = float(lis[i])
        originalDataInner.append(val)
        # Squaring each of the datapoints
        dataPointsInner.append(np.math.pow(val, 2))      
    temp = float(lis[len(lis) - 1])
    target.append(temp)
    originalDataOuter.append(originalDataInner)
    dataPointsOuter.append(dataPointsInner)
 
# Fit the given model
c = svm.SVC(kernel='linear')
c.fit(dataPointsOuter, target)

# Get the hyperplane 
wVector = c.coef_[0]
a = -wVector[0] / wVector[1]
x = np.linspace(-100, 100)
hyperplane = a * x - (c.intercept_[0]) / wVector[1]
print "---------------------Hyperplane----------------------"
print "Intercept => ", -(c.intercept_[0]) / wVector[1]
print "Slope => ", a
print "------------------Equation Value-------------------------"
eqn = (np.multiply(a,dataPointsOuter))-(c.intercept_[0]) / wVector[1]
print eqn
print "------------Support Vectors for the hyperplane--------------\n", c.support_vectors_

bias = c.support_vectors_[0]
lowerMargin = a * x + (bias[1] - a * bias[0])
bias = c.support_vectors_[-1]
upperMargin = a * x + (bias[1] - a * bias[0])

preimageIndices = c.support_

print "--------------Indices of the Preimages----------------\n", preimageIndices
print "------------PreImages of Support Vectors--------------\n", originalDataOuter[preimageIndices[0]]
print originalDataOuter[preimageIndices[1]]
print originalDataOuter[preimageIndices[2]]
print "------------------------------------------------------\n"

# Plot the fattest margin 
plt.plot(x, hyperplane, 'k-')
plt.plot(x, lowerMargin, 'k--')
plt.plot(x, upperMargin, 'k--')

plt.scatter(c.support_vectors_[:, 0], c.support_vectors_[:, 1],s=80, facecolors='none')

i = 0
for row in dataPointsOuter:
    x = row[0]
    y = row[1]
    plt.scatter(x, y, c=target[i])
    i += 1

# Writing to text file
fw = open('SVMOutput.txt','w')

fw.write("-----------------Hyperplane------------------\n")
fw.write("Intercept => ")
temp = -(c.intercept_[0]) / wVector[1]
fw.write("%10f\n" % temp)
fw.write("Slope => ")
fw.write("%10f\n" % a)
fw.write("------------------------------------------------------\n")
for i in eqn:
    fw.write("%s\n" % i)

fw.write("------------Support Vectors for the hyperplane--------------\n")
for i in c.support_vectors_:
    fw.write("%s\n" % i)

fw.write("--------------Indices of the Preimages----------------\n")
fw.write("%s\n" % preimageIndices)
fw.write("------------PreImages of Support Vectors--------------\n")
fw.write("%s\n" % originalDataOuter[preimageIndices[0]])
fw.write("%s\n" % originalDataOuter[preimageIndices[1]])
fw.write("%s\n" % originalDataOuter[preimageIndices[2]])
fw.write("------------------------------------------------------\n")

fw.close()

plt.axis('tight')
plt.show()