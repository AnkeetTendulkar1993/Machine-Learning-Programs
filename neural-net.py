# Implementation of Neural Networks

import numpy as np
import matplotlib.pyplot as plt
import time


def plot_data(data, labels):
	plt.scatter(data[:,0], data[:,1], s=10, c=labels, edgecolors='none')
	plt.show()


def prediction(data, labels,w,b):
	z = np.dot(data, w)+b
	y = 1/(1+np.exp(-z))
        prediction = y > 0.5
	return prediction

def learn_neuron(data, labels):
	w = 0.01*np.random.randn(2,1)	
	b = 0	
	epsilon = 0.0001	
	x = data
	t = labels

	for i in xrange(1000):
		print data.shape
		print labels.shape
		print w.shape
		print b
		z = np.dot(x, w)+b
		y = 1/(1+np.exp(-z))

		prediction = y > 0.5	
		acc = np.mean(prediction.astype(int)==t)
                
		L = 0.5*np.sum(np.square(y-t))
	
		dLbydy = y-t
		dLbydz = dLbydy * y * (1-y)
		dLbydw = np.dot(x.T, dLbydz)  
		dLbydb = np.sum(dLbydz)

		dw = -epsilon * dLbydw
		db = -epsilon * dLbydb

		w = w + dw
		b = b + db
	result = []
	result.append(w)
	result.append(b)
	return result
	plt.ioff()
	#plt.show()	



if __name__ == '__main__':

    fileP = open("svm","rU")
    temp = [r.split(' ')  for r in fileP.read().split('\n')]
    #print temp
    dataPoints = [[]]
    del(temp[100])
    dataPoints =  [ [float(t[0]),float(t[1])] for t in temp]
    label=[]
    for t in temp:	 
	print t
    	if (cmp(t[2],'-1') == 0):
			label.append([0])
	else: 
			label.append([1])
    print label
    X=np.array(dataPoints)
    y=np.array(label)
    print X.shape
    result = learn_neuron(X[46:71],y[46:71]) 
    print "Results"
    count = 0
    for i in range(0,100):
       pred = prediction(X[i],y[i],result[0],result[1])
       print "The given label and the label obtained is :" +str(int(y[i])) +"and" +str(int(pred))
       if(y[i] == pred):
		count = count + 1
    print "The accuracy of prediction is as follows :"
    print count