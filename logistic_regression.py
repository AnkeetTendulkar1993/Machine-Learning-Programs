# Implementation of Logistic Regression

import sys 
import re
import json
import numpy as np 
import math

def sigmoid(wx):
	temp =  wx
	den = 1.0 + np.power(math.e,-temp)
	d = 1.0 / den
	return d

def ln(x, minval=0.000000001):
    return np.log(x.clip(min=minval))


def getCost(h, label):
    label = np.squeeze(label)
    part1 = label * ln(h)
    part2 = (1-label) * ln(1 - h)
    cost_array = -part1 - part2
    print "the cost is" + str(np.mean(cost_array))
    return np.mean(cost_array)


if __name__ == '__main__':
	data = open(sys.argv[1])
	x = np.array([1,1,1])
	label = np.array([1])
	for line in data:
		coordinate = line.split(',')
		temp1 = [float(coordinate[0]), float(coordinate[1]), float(coordinate[2])]
		temp2 = [float(coordinate[4])]
		if (cmp(temp2,[-1.0]) == 0):
			temp2 = [0.0]
		print temp2
		x = np.vstack([x, temp1])
		label = np.vstack([label, temp2])
	x = np.delete(x,0,0)
        x = (x - np.mean(x, axis=0)) / np.std(x, axis=0)
    	s=(50,1)
    	onesCol=np.ones(s)
    	x=np.concatenate((onesCol,x), axis=1)
	label = np.delete(label,0,0)
	(m,n) = x.shape
	print (m,n)
	print label.shape
	print "x is"
	#x = np.asmatrix(x)
        x.astype(float)
	print x	
	print "label is"
	#label = np.asmatrix(label)
	label.astype(float)
	print label
	weight = [float(0),float(1),float(1),float(1)]
	weight = np.array(weight)
	#weight = np.asmatrix(weight)
	#weight = weight.T
	print "weight is"
	print weight
	cost = 1
	converge_diff =.0001
	diff_cost = 1
	alpha = 0.01
	k = 1
	i = 0
	while  diff_cost > converge_diff:
		old_cost = cost
		h = sigmoid(x.dot(weight))
		#print "h is"
		#print h
		error = np.squeeze(h) - np.squeeze(label)
		#print "error is"
		#print error
		weight = weight - ((alpha*(error.dot(x))))
		#print "new weight is"
		print k 
		print weight
		cost = getCost(h,label)
		diff_cost = old_cost - cost
	 	k = k + 1
