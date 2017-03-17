from __future__ import division
import numpy as np
import sys
from collections import defaultdict
import math

# classvals is a numpy size n array of class values
# class values here are Y values thresholded into quintiles
# Return the entropy of classvals
def entropy(classvals):
	entropy = 0
	uniqueDict = {}
	for x in classvals:
		if x not in uniqueDict:
			uniqueDict[x] = 1
		else:
			uniqueDict[x] += 1

	probabilities = {}
	for key in uniqueDict:
		prob = float(uniqueDict[key]) / float(len(classvals))
		probabilities[key] = prob

	for key in probabilities:
		if probabilities[key] > 0:
			entropy += - (probabilities[key] * math.log10(probabilities[key]) / math.log10(5))
	return entropy

# # colvals is a numpy size n array of column values
# # That is, a feature column with the features thresholded into quintiles
# # colvals indices correspond to those in the size n classvals array
# # Return expected entropy of classvals after splitting on colvals
def expected_entropy(colvals, classvals):
	uniqueDict = dict()
	for x in colvals:
		if x not in uniqueDict:
			uniqueDict[x] = 1
		else:
			uniqueDict[x] += 1

	probabilities = dict()
	for key in uniqueDict:
		prob = float(uniqueDict[key]) / float(colvals.shape[0])
		probabilities[key] = prob

	indices_dict = dict()
	for key in probabilities:
		#find all indexes where key in colvals occurs
		indices = []
		index = 0
		for num in colvals:
			if num == key:
				indices.append(index)
			index+=1
		indices_dict[key] = indices
	total = 0
	for key in indices_dict:
		total += probabilities[key] * entropy(indices_dict[key])
	return total

if __name__ == '__main__':
	# Extract online_shares dataset
	fp = open(sys.argv[1], 'r')
	lines = fp.readlines()
	features = [st.strip() for st in lines[0].split(',')]
	features.pop() # Get rid of shares label
	data = np.genfromtxt(sys.argv[1], delimiter=',')

	X = data[1:, :data.shape[1]-1]
	Y = data[1:, data.shape[1]-1]

	# Get quintiles
	Xpercs = np.array(np.percentile(X,[20,40,60,80,100], axis=0))
	Ypercs = np.array(np.percentile(Y,[20,40,60,80,100]))

	# Threshold everything into quintiles
	for i in range(X.shape[0]):
		for k in range(Xpercs.shape[1]):
			for j in range(Xpercs.shape[0]):
				if X[i,k] <= Xpercs[j,k]:
					X[i,k] = Xpercs[j,k]
					break

	for i in range(len(Y)):
		for j in range(len(Ypercs)):
			if Y[i] <= Ypercs[j]:
				Y[i] = Ypercs[j]
				break
	
	# Compute all information gains
	y_entropy = entropy(Y)	
	infogains = np.zeros((X.shape[1]))
	for i in range(len(infogains)):
		infogains[i] = y_entropy-expected_entropy(X[:,i],Y)

	# Sort infogains descending
	sorted_inds = np.argsort(infogains)[::-1]

	assert(len(infogains)==len(features))
	for i in range(len(sorted_inds)):
		print features[sorted_inds[i]], ',', infogains[sorted_inds[i]]


