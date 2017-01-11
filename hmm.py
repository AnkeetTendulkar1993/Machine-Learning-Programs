# Implementation of Hidden Markov Models

import sys 
import re 
import math
import matplotlib.pyplot as plt
import numpy as np
#get possible movements for a certain position 
#returns an array of tuples which are the i, j of the cells you can go to
def get_transitions(grid , i, j):
	moves = []
	#you cant even be there
	if grid[i][j] == 0:
		return moves
	#number 1 to 9 columns have a possible left cell - 0 does not have
	if j > 0 and j <=9: 		
		if grid[i][j-1] == 1:
			moves.append([i,j-1])
	#number 0 to 8 columns have a possible right cell - 9 does not have
	if j >= 0 and j < 9:	
		if grid[i][j+1] == 1:
			moves.append([i,j+1])
	#rows 1 to 9 have a top cell - o does not have 
	if i > 0 and i <=9: 		
		if grid[i-1][j] == 1:
			moves.append([i-1,j])
	#rows 0 to 8 have a down cell - 9 does not have 
	if i >=0 and i < 9: 		
		if grid[i+1][j] == 1:
			moves.append([i+1,j])
	return moves	
	

def initialize(n):
	each_state_transition = []		
	i = 0 
	while i < n:
		each_state_transition.append(0)
		i =  i + 1
	#print each_state_transition
	return each_state_transition



if __name__ == '__main__':
	grid = []
	a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	grid.append(a)
	a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	grid.append(a)
	a = [1, 1, 0, 0, 0, 0, 0, 1, 1, 1]
	grid.append(a)
	a = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1]
	grid.append(a)
	a = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1]
	grid.append(a)
	a = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1]
	grid.append(a)
	a = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1]
	grid.append(a)
	a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	grid.append(a)
	a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	grid.append(a)
	a = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
	grid.append(a)
	#print grid 
	noise = []
	a = [6.29711934499524,5.89798026180419,5.50487473660225,6.66926691757846]
	noise.append(a)
	a = [5.55617105284999,7.14846859129049,4.26776888864906,6.80366418635034]
	noise.append(a)
	a = [7.56526520813249,9.36656419021787,4.32876429991063,5.34864267984477]
	noise.append(a)
	a = [9.5118768189536,10.0483738149828,3.70044108449547,6.63594042198103]
	noise.append(a)
	a = [5.99003335814561,10.655826135343,2.7620662779914,5.80249827656104]
	noise.append(a)
	a = [9.27694058691455,10.2305482684336,2.57766309378204,5.37836394257541]
	noise.append(a)
	a = [7.96759239165615,13.0940213788512,1.90070680421102,9.43043572304003]
	noise.append(a)
	a = [6.40043749794988,8.17104806326276,3.90838998574875,8.79060391152427]
	noise.append(a)
	a = [4.9597335820898,10.3348832630105,3.60516126931873,7.2157907900465]
	noise.append(a)
	a = [3.77302315182655,9.76524026071066,4.37773108161243,8.82027211111639]
	noise.append(a)
	a = [3.26328625549544,7.59841629030013,4.3316857153888,8.54160160853063]
	noise.append(a)
	#parse this into a transition matrix 
	i = 0 
	j = 0
	count_states = 0
	free_states = []
	free_states_label = {}
	free_states_lookup = {}
	while i < 10:
		j = 0
		while j < 10:
			state = []
			if(grid[i][j] == 1):
				count_states = count_states + 1
				state.append(i)
				state.append(j)
				free_states.append(state)	
			j = j + 1		
		i = i + 1
	#print count_states
	#print free_states
	i = 1
	for free_state in free_states:
		free_states_label[tuple(free_state)] = i
		i = i + 1
	i = 1
	for free_state in free_states:
		free_states_lookup[i] = free_state
		i = i + 1
	#print sorted(free_states_label, key=free_states_label.get)
	transition_matrix = []	
	each_state_transition = []

	#Filling the transition matrix
	i = 0
	j = 0
	#print len(free_states)
	while i < 10:
		j = 0
		while j < 10:
			if grid[i][j] == 1:
				#print free_states_label[(i,j)]
				moves = get_transitions(grid , i, j )
				num_of_moves = float(len(moves))
				probability = float(1.0/num_of_moves)
				each_state_transition = initialize(count_states)
				for move in moves:
					x = move[0]
					y = move[1]
					state_number = free_states_label[(x,y)]
					each_state_transition[state_number - 1] = probability
					#print each_state_transition
				transition_matrix.append(each_state_transition)
			#print each_state_transition
			#print probability
			j = j +1
		i = i + 1

	
	
	precision = 0.1
	maximum_euclidean = round(math.sqrt(100+100),1)
	#print maximum_euclidean
	noise_mapping = {}
	i = 0
	count = 0
	while i <= maximum_euclidean:
		noise_mapping[i] = count
		count = count +1
		i = i + 0.1
		i = round(i,1)
	#print sorted(noise_mapping, key=noise_mapping.get)
	#print noise_mapping
	
	tower1 = [0, 0]
	t1 = []
	i = 1
	while i <= count_states:
		condition_probablity_each_state = initialize(maximum_euclidean*10)
		#print len(condition_probablity_each_state)
		state = free_states_lookup[i]
		#print state
		distance = math.sqrt(((state[0] - tower1[0])* (state[0] - tower1[0])) +((state[1] - tower1[1])* (state[1] - tower1[1])))
		#print distance 
		#print 0.7*distance
		#print 1.3*distance
		range1 = round(0.7*distance , 1)
		range2 = round(1.3*distance , 1)
		length_of_range = ((range2-range1) + 0.1)*10
		#print range1
		#print range2
		#print length_of_range
		probability = float(1.0/length_of_range)
		#print probability
		k = range1
		while k <= range2 and k<=maximum_euclidean :
			condition_probablity_each_state[noise_mapping[k]-1] = probability
			k = k+0.1
			k = round(k,1)
			#print k
		#print condition_probablity_each_state
		t1.append(condition_probablity_each_state)
		i = i + 1

	tower2 = [0, 9]
	t2 = []
	i = 1
	while i <= count_states:
		condition_probablity_each_state = initialize(maximum_euclidean*10)
		#print len(condition_probablity_each_state)
		state = free_states_lookup[i]
		#print state
		distance = math.sqrt(((state[0] - tower2[0])* (state[0] - tower2[0])) +((state[1] - tower2[1])* (state[1] - tower2[1])))
		#print distance 
		range1 = round(0.7*distance , 1)
		range2 = round(1.3*distance , 1)
		length_of_range = ((range2-range1) + 0.1)*10
		probability = float(1.0/length_of_range)
		k = range1
		while k <= range2 and k<=maximum_euclidean :
			condition_probablity_each_state[noise_mapping[k]-1] = probability
			k = k+0.1
			k = round(k,1)
		t2.append(condition_probablity_each_state)
		i = i + 1
	
	tower3 = [9, 0]
	t3 = []
	i = 1
	while i <= count_states:
		condition_probablity_each_state = initialize(maximum_euclidean*10)
		state = free_states_lookup[i]
		distance = math.sqrt(((state[0] - tower3[0])* (state[0] - tower3[0])) +((state[1] - tower3[1])* (state[1] - tower3[1])))
		range1 = round(0.7*distance , 1)
		range2 = round(1.3*distance , 1)
		length_of_range = ((range2-range1) + 0.1)*10
		probability = float(1.0/length_of_range)
		k = range1
		while k <= range2 and k<=maximum_euclidean :
			condition_probablity_each_state[noise_mapping[k]-1] = probability
			k = k+0.1
			k = round(k,1)
		t3.append(condition_probablity_each_state)
		i = i + 1
		
	tower4 = [9, 9]
	t4 = []
	i = 1
	while i <= count_states:
		condition_probablity_each_state = initialize(maximum_euclidean*10)
		state = free_states_lookup[i]
		distance = math.sqrt(((state[0] - tower4[0])* (state[0] - tower4[0])) +((state[1] - tower4[1])* (state[1] - tower4[1])))
		range1 = round(0.7*distance , 1)
		range2 = round(1.3*distance , 1)
		length_of_range = ((range2-range1) + 0.1)*10
		probability = float(1.0/length_of_range)
		k = range1
		while k <= range2 and k<=maximum_euclidean :
			condition_probablity_each_state[noise_mapping[k]-1] = probability
			k = k+0.1
			k = round(k,1)
		t4.append(condition_probablity_each_state)
		i = i + 1

	time_total = len(noise)
	states_total = len(free_states)
	prob = []
	back = []
	#initialize them to 0
	state = 0
	while state < len(free_states):
		a = initialize(time_total)
		prob.append(a)
		state = state+1
	state = 0
	while state < len(free_states):
		a = initialize(time_total)
		back.append(a)
		state = state+1
	time = 0 #this mean interval one 
	#array na so it is 0
	state = 0

	free_states_lookup[-1] = [10,10]
	free_states_lookup[0] = [10,10]
	while state < 87:
		n1_index = int(round(noise[0][0],1)*10)
		n2_index = int(round(noise[0][1],1)*10)
		n3_index = int(round(noise[0][2],1)*10)
		n4_index = int(round(noise[0][3],1)*10)
		prob[state][0] = float(1.0/87.0) * t1[state][n1_index] * t2[state][n2_index] * t3[state][n3_index] * t4[state][n4_index]  
		#backpointer points to any of the neigbhoring cells near this one which is free 
		#so just search for its neighbor and keep track
		coordinates = free_states_lookup[state+1]
		moves = get_transitions(grid , coordinates[0], coordinates[1])
		state_0 = free_states_label[(moves[0][0],moves[0][1])]
		back[state][0] = state_0
		state = state + 1
	time = 1 
	while time < 11:
		state  = 0
		while state < states_total:
			n1_index = int(round(noise[time][0],1)*10)
			n2_index = int(round(noise[time][1],1)*10)
			n3_index = int(round(noise[time][2],1)*10)
			n4_index = int(round(noise[time][3],1)*10)
			previous_time = time - 1
			x = 0
			maximum = 0.0
			back_value = -1
			while x < states_total:
				value = prob[x][previous_time]*transition_matrix[x][state]*t1[state][n1_index] * t2[state][n2_index] * t3[state][n3_index] * t4[state][n4_index]
				if value > maximum:
					maximum = max(maximum,value)
				x = x + 1
			prob[state][time] = maximum
			maximum = 0.0
			back_value = -1
			x = 0
			while x < states_total:
				value = prob[x][previous_time]*transition_matrix[x][state]
				if value > maximum:
					maximum = max(maximum,value)
					back_value = x
				x = x + 1
			back[state][time] = back_value
			state = state +1
		time = time+1
	
	#print free_states_lookup
	path = {}
	final_states = []
	#find the final state with max probability
	maximum = 0.0
	state = 0 
	final_state = state
	while state < 87:
		if prob[state][10] > maximum:
			maximum = prob[state][10]
			final_state = state
		state = state + 1
	final_states.append(free_states_lookup[final_state+1])
	path[11] = free_states_lookup[final_state+1]
	
	
	i = 10
	while i > 0:		
		back_state = back[final_state][i]
		path[i] = free_states_lookup[back_state+1]
		final_state = back_state
		i = i - 1
	print path
	path_plot=path.values()
	x=[]
	y=[]
	for point in path_plot:
		x.append(point[0])
		y.append(point[1])
	fig = plt.figure()
	ax = fig.gca()
	ax.set_xticks(np.arange(1,10,1))
	ax.set_yticks(np.arange(1,10,1))
	plt.grid()
	plt.axis([0, 10, 0, 10])
	plt.plot(x, y, marker='o', linestyle='--', color='b', label='Path')
	plt.plot(x[0],y[0],marker='o',color='g',label="Start")
	plt.plot(x[10],y[10],marker='o',color='r',label="Finish")
	plt.title('Optimum Path')
	plt.legend()
	plt.show()
		
	
