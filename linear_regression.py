# Implementation of Linear Regression

import sys 
import re
import json
import numpy as np 
from pylab import plot,show
if __name__ == '__main__':
	data = open(sys.argv[1])
	x = np.array([1,1,1])
	h = np.array([1])
	for line in data:
		coordinate = line.split(',')
		temp1 = [1,float(coordinate[0]), float(coordinate[1])]
		temp2 = [float(coordinate[2])]
		x = np.vstack([x, temp1])
		h = np.vstack([h, temp2])
	
	x = np.delete(x,0,0)
	h = np.delete(h,0,0)
	#print x.shape
	#print h.shape
	#print "x is"
	x = np.asmatrix(x)
        x.astype(float)
	#print x	
	#print "h is"
	h = np.asmatrix(h)
	h.astype(float)
	#print h
	#find the inverse of x
	print "weight matrix is"
        #print x.T * x
	#print np.linalg.inv(np.dot(x.T,x))
        #inv( xt* x)* xt * y
	theta = np.dot(np.dot((np.linalg.inv(np.dot(x.T,x))),x.T),h)
	print theta
