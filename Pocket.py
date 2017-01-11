# Implementation of the Pocket Algorithm

import random as rand
import numpy as np
import matplotlib.pyplot as plt

f = open('linear.txt','r')
data = f.readlines()

# Storig the input data 
dimensionsOuter =[]        
for x in data:
    lis = x.rstrip().split(",")
    dimensionsInner = []
    for i in range(0,len(lis)):       
        if (i != 3):
            temp = float(lis[i])
            dimensionsInner.append(temp)            
    dimensionsOuter.append(dimensionsInner)

w = []

# Initializing the value of w
w.append(0.0)
w.append(0.0)
w.append(0.0)
w.append(0.0)

# If you want to initialize to random values uncomment the following lines
# w.append(rand.uniform(0.0,1.0))
# w.append(rand.uniform(0.0,1.0))
# w.append(rand.uniform(0.0,1.0))
#w.append(rand.uniform(0.0,1.0))

# Initializing basic parameters
rate = 0.001
iterationNumber = 0
errorList = []

while(iterationNumber != 500):
    e = 0
    for i in range(0, len(dimensionsOuter)):
        #print i
        firstX = 1.0
        x = dimensionsOuter[i]
        x = [firstX] + x
        desiredOutput = x[4]
        del x[len(x) - 1]
        result = np.dot(w,x)
        if result >= 0:
            networkOutput = 1.0
        else: 
            networkOutput = -1.0
        error = desiredOutput - networkOutput
        correction = rate * error
        
        if error != 0:
            newX = []
            newX[:] = [(x[i]*correction) for i in range(0,len(x))]
            w = np.add(w,newX)
            e += 1

    iterationNumber += 1
    errorList.append(e)
    if e == 0:
        break

# Displaying the output
print "Weight = ", w
print "Iterations = ", iterationNumber
print "Error = ", e

# Writing to the output file
fw = open('PocketOutput.txt','w')

fw.write("Weight = ")
for item in w:
    fw.write("%s " % item) 
fw.write("\nError = ")
fw.write("%d " % e)   
fw.write("\nIterations = ")
fw.write("%d " % iterationNumber)  

fw.close()

# Plotting the misclassifications against iterations
plt.plot(errorList)
plt.axis([0,500,0,50])
plt.ylabel('Misclassifications') 
plt.xlabel('Iterations') 
plt.show()