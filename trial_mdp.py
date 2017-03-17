import numpy as np
import sys
import math

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

def iterate(matrix, inputs):
	count = 0
	while(True):
		algorithm(matrix, inputs)
		if count == 50:
			break
		count += 1

def algorithm(matrix, inputs):
	mult = inputs[0]
	add = inputs[1]
	optimal_dir = inputs[2]
	clockwise = inputs[3]
	opposite = inputs[4]
	counter_clockwise = inputs[5]
	num_rows = inputs[6]
	num_cols = inputs[7]
	row_now = 0
	col_now = 0

	count = 0
	for row in range(num_rows):
		for col in range(num_cols):
			north = 0
			south = 0
			east = 0
			west = 0

			if row-1 >= 0: #north
				if matrix[row-1][col] != "x":
					north = matrix[row-1][col]
				else:
					north = matrix[row][col]
			if row+1 < num_rows: #south
				if matrix[row+1][col] != "x":
					south = matrix[row+1][col]
				else:
					south = matrix[row][col]
			if col+1 < num_cols: #east
				if matrix[row][col+1] != "x":
					east = matrix[row][col+1]
				else:
					east = matrix[row][col]
			if col-1 >= 0: #west
				if matrix[row][col-1] != "x":
					west = matrix[row][col-1]
				else:
					west = matrix[row][col]

			reward_val = 0
			if matrix[row][col] != "x":
				reward_val = matrix[row][col] 

			try_north = (float(north) * optimal_dir) + (float(south) * opposite) + (float(east) * clockwise) + (float(west) * counter_clockwise)
			try_south = (float(south) * optimal_dir) + (float(north) * opposite) + (float(east) * counter_clockwise) + (float(west) * clockwise)
			try_east = (float(east) * optimal_dir) + (float(west) * opposite) + (float(north) * counter_clockwise) + (float(south) * clockwise)
			try_west = (float(west) * optimal_dir) + (float(east) * opposite) + (float(north) * clockwise) + (float(south) * counter_clockwise)

			max_val = max(try_north, try_south, try_east, try_west)

			# if matrix[row][col] != "x":
			# 	max_val += matrix[row][col]

			if matrix[row][col] != "x" and matrix[row][col] != -1 and matrix[row][col] != 1:
				val = add + (max_val * mult)
				matrix[row][col] = val

			count += 1
			# if count == 50000:
			# 	break
	print(matrix)


def main():
	matrix, inputs = parse_file(sys.argv[1])
	iterate(matrix, inputs)
	#algorithm(matrix, inputs)

if __name__ == '__main__':
	main()
