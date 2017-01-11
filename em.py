# Implementation of Expectation Maximization Algorithm

import sys 
import re
import json
import numpy as np 
import math
import matplotlib.pyplot as plt

def getProbability(x,mean,cv,d):
	a = (2.0*math.pi) ** (d/2)
	b = 1.0/a
	c = np.linalg.det(cv)**0.5
	d = 1.0/c
	inv_cv = np.linalg.inv(cv)
	constant = -0.5
	diff = (np.array(x) - np.array(mean))
	#print diff
	diff_t = diff.T
	#print diff_t
	value = (diff_t.dot(inv_cv)).dot(diff)
	#print value
	value_1 = constant*value
	#print value_1
	exponent_component = math.pow(math.e,value_1)
	#print exponent_component
	probability = b*d*exponent_component
	#sprint probability
	return probability
	

if __name__ == '__main__':
	points = []
	data = open(sys.argv[1])
	x_all = []
	y_all = []
	for line in data:
		point = []	
		coordinate = line.split(',')
		x = float(coordinate[0])
		y = float(coordinate[1])
		x_all.append(x)
		y_all.append(y)
		point.append(x)
		point.append(y)
		points.append(point)
    	mean_1 = points[0]
	mean_2 = points[1]
	mean_3 = points[2]
	theta_1 = float(1.0/3.0)
	theta_2 = float(1.0/3.0)
	theta_3 = float(1.0/3.0)
	cv1 = np.zeros((2,2) , dtype=np.float)
	np.fill_diagonal(cv1, 1)
	cv2 = np.zeros(shape = (2,2), dtype=np.float)
	np.fill_diagonal(cv2, 1)
	cv3 = np.zeros(shape = (2,2), dtype=np.float)
	np.fill_diagonal(cv3, 1)	
	old_mean_1 = [0.0,0.0]
	old_mean_2 = [3.0,3.0]
	old_mean_3 = [10.0,10.0]
	old_cv1 = np.zeros((2,2) , dtype=np.float)
	np.fill_diagonal(old_cv1, 1)
	old_cv2 = np.zeros(shape = (2,2), dtype=np.float)
	np.fill_diagonal(old_cv2, 1)
	old_cv3 = np.zeros(shape = (2,2), dtype=np.float)
	np.fill_diagonal(old_cv3, 1)	

	done = False
	iter = 0 
	while (iter < 10):
		i = 0	
		#print "theta value is" +str(theta_1)
		z1 = []
		z2 = []
		z3 = []
		while i < 150:
			#print "********************************************"
			zi1 = float(theta_1*getProbability(points[i],mean_1,cv1,2))
			#print str(points[i])+"zi1"+str("%.2f" % zi1)	
			#prob1.append(getProbability(points[i],mean_1,cv1,2))
			z1.append(zi1)
			zi2 = float(theta_2*getProbability(points[i],mean_2,cv2,2))
			z2.append(zi2)
			zi3 = float(theta_3*getProbability(points[i],mean_3,cv3,2))
			z3.append(zi3)
			i = i+1 
		#print z1
			#print " z1 sum is"+str(np.sum(np.array(z1).astype(np.float), dtype=np.float))
		#print z2
		#print z3
	
		theta_1 = (np.sum(np.array(z1).astype(np.float)))/150.0
		print theta_1
		sum_x = 0.0
		sum_y = 0.0
		point = 0
		while point < 150:
			sum_x = sum_x + points[point][0]*z1[point]
			sum_y = sum_y + points[point][1]*z1[point]
			point = point + 1
		mean_1 = []
		denominator = np.sum(np.array(z1).astype(np.float))
		mean_1.append(sum_x/denominator)
		mean_1.append(sum_y/denominator)
		print mean_1
		point = 0
		weight_sum = np.zeros((2,2) , dtype=np.float)
		while point < 150:
			diff = ((np.array(points[point]) - np.array(mean_1)))
			#print  (diff.T)
		        diff = np.asmatrix(diff)
			#print z1[point]*np.cov(np.array(x_all),np.array(y_all))
			covar = (z1[point]*(diff.T)).dot(diff)
			weight_sum = weight_sum + covar
			point = point + 1
		cv1 = (1.0/denominator)*weight_sum
		print "weighted covar"
		print cv1

		theta_2 = (np.sum(np.array(z2).astype(np.float)))/150.0
		print theta_2
		sum_x = 0.0
		sum_y = 0.0
		point = 0
		while point < 150:
			sum_x = sum_x + points[point][0]*z2[point]
			sum_y = sum_y + points[point][1]*z2[point]
			point = point + 1
		mean_2 = []
		denominator = np.sum(np.array(z2).astype(np.float))
		mean_2.append(sum_x/denominator)
		mean_2.append(sum_y/denominator)
		print mean_2
		point = 0
		weight_sum = np.zeros((2,2) , dtype=np.float)
		while point < 150:
			diff = ((np.array(points[point]) - np.array(mean_2)))
			#print  (diff.T)
		        diff = np.asmatrix(diff)
			#print z1[point]*np.cov(np.array(x_all),np.array(y_all))
			covar = (z2[point]*(diff.T)).dot(diff)
			weight_sum = weight_sum + covar
			point = point + 1
		cv2 = (1.0/denominator)*weight_sum
		print "weighted covar"
		print cv2

		
		theta_3 = (np.sum(np.array(z3).astype(np.float)))/150.0
		print theta_3
		sum_x = 0.0
		sum_y = 0.0
		point = 0
		while point < 150:
			sum_x = sum_x + points[point][0]*z3[point]
			sum_y = sum_y + points[point][1]*z3[point]
			point = point + 1
		mean_3 = []
		denominator = np.sum(np.array(z3).astype(np.float))
		mean_3.append(sum_x/denominator)
		mean_3.append(sum_y/denominator)
		print mean_3
		point = 0
		weight_sum = np.zeros((2,2) , dtype=np.float)
		while point < 150:
			diff = ((np.array(points[point]) - np.array(mean_3)))
			#print  (diff.T)
		        diff = np.asmatrix(diff)
			#print z1[point]*np.cov(np.array(x_all),np.array(y_all))
			covar = (z3[point]*(diff.T)).dot(diff)
			weight_sum = weight_sum + covar
			point = point + 1
		cv3 = (1.0/denominator)*weight_sum
		print "weighted covar"
		print cv3
		iter = iter + 1
	cluster1_x= []
	cluster1_y= []
	cluster2_x = []
	cluster2_y = []
	cluster3_x = []
	cluster3_y = []

	i = 0
	while i < 150:	
		max = -1
		belongs = -1
		if z1[i]> max:
			max = z1[i]
			belongs = 1
		if z2[i]> max:
			max = z2[i]
			belongs = 2
		if z3[i]> max:
			max = z3[i]
			belongs = 3
		if belongs == 1:
			cluster1_x.append(points[i][0])
			cluster1_y.append(points[i][1])
		if belongs == 2:
			cluster2_x.append(points[i][0])
			cluster2_y.append(points[i][1])
		if belongs == 3:
			cluster3_x.append(points[i][0])
			cluster3_y.append(points[i][1])
		i = i + 1
	
