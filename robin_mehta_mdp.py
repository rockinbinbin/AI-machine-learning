from __future__ import print_function
import numpy as np
import sys
import math
import copy

def parse_file(path):
	mult = 0
	add = 0
	optimal_dir = 0
	clockwise = 0
	opposite = 0
	counter_clockwise = 0
	num_rows = 0
	num_cols = 0

	line_num = 0
	with open(path,'r') as data:
		for line in data.read().split('\n'):
			if line_num == 0:
				mult = float(line)
			if line_num == 1:
				add = float(line)
			if line_num == 2:

				word_num = 0
				for word in line.split(" "):
					if word_num == 0:
						optimal_dir = float(word)
					if word_num == 1:
						clockwise = float(word)
					if word_num == 2:
						opposite = float(word)
					if word_num == 3:
						counter_clockwise = float(word)
					word_num += 1

			if line_num == 3:
				for point in line.split(" "):
					num_cols += 1
			line_num += 1
		num_rows = line_num - 3
	
	Matrix = [[0 for x in range(num_cols)] for y in range(num_rows)] 
	with open(path, 'r') as data:
		line_num = 0
		for line in data.read().split('\n'):
			if line_num >= 3:
				row_count = line_num - 3
				col_count = 0

				for word in line.split(" "):
					if word == "*":
						word = 0
					if word != "x":
						Matrix[row_count][col_count] = float(word)
					else:
						Matrix[row_count][col_count] = word

					col_count += 1
				#row_count += 1
			line_num += 1

	inputs = [mult, add, optimal_dir, clockwise, opposite, counter_clockwise, num_rows, num_cols]
	return Matrix, inputs

def algorithm(matrix, inputs):
	mult = inputs[0]
	add = inputs[1]
	optimal_dir = inputs[2]
	clockwise = inputs[3]
	opposite = inputs[4]
	counter_clockwise = inputs[5]
	num_rows = inputs[6]
	num_cols = inputs[7]
	count = 0
	updated_matrix = copy.deepcopy(matrix)
	#print("mult: ", mult, "add: ", add, "optimal: ", optimal_dir, "clockwise: ", clockwise, "opposite: ", opposite, "counter: ", counter_clockwise, "numrows: ", num_rows, "numcols: ", num_cols)
	#print(matrix)
	while(True):
		for row, row_val in enumerate(matrix):
			for col, col_val in enumerate(row_val):
				if matrix[row][col] != "x" and matrix[row][col] != -1 and matrix[row][col] != 1:
					north = matrix[row][col]
					south = matrix[row][col]
					east = matrix[row][col]
					west = matrix[row][col]

					if matrix[row-1] >= 0 and matrix[row-1][col] != "x": #north
						north = matrix[row-1][col]
					if row+1 < num_rows and matrix[row+1][col] != "x": #south
						south = matrix[row+1][col]
					if col+1 < num_cols and matrix[row][col+1] != "x": #east
						east = matrix[row][col+1]
					if col-1 >= 0 and matrix[row][col-1] != "x": #west
						west = matrix[row][col-1]

					#print("north: ", north, "south: ", south, "east: ", east, "west: ", west)
					try_north = (north * optimal_dir) + (south * opposite) + (east * clockwise) + (west * counter_clockwise)
					try_south = (south * optimal_dir) + (north * opposite) + (east * counter_clockwise) + (west * clockwise)
					try_east = (east * optimal_dir) + (west * opposite) + (north * counter_clockwise) + (south * clockwise)
					try_west = (west * optimal_dir) + (east * opposite) + (north * clockwise) + (south * counter_clockwise)
					max_val = np.amax(np.array([float(try_north), float(try_south), float(try_east), float(try_west)]))
					#print("max_val: ", max_val)
					val = add + (max_val * mult)
					updated_matrix[row][col] = val
					#print("val: ", val)

		#print("updated matrix: ", updated_matrix, "\n", "matrix: ", matrix, "\n\n")
		matrix = copy.deepcopy(updated_matrix)
		#print("updated matrix: ", updated_matrix, "\n", "matrix: ", matrix)
		if count == 100:
			break
		count+=1
	print(matrix)

def main():
	matrix, inputs = parse_file(sys.argv[1])
	#runIterations(matrix, inputs)
	algorithm(matrix, inputs)

if __name__ == '__main__':
	main()
