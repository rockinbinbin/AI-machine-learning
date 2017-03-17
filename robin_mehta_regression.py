from __future__ import print_function
import numpy as np
import sys

# Given coefficients w,
# generate noisy random data points X, Y
# Where Y is approximately (X transpose)*w
# This is used to test gradient_descent
def generate_data(npoints, w):
	dim = np.size(w)
	X = np.random.uniform(-10, 10, (dim, npoints))
	Y = np.dot(X.T, w)
	err = np.random.normal(0, 1, (npoints))
	return X, Y+err


# Returns the exact best fit w to the data
def exact_solution(X, Y):
	transform = np.dot(X, X.T)
	inverse = np.add(np.eye(X.shape[0]), transform)
	inverse = np.linalg.inv(inverse)
	xy = np.dot(X, Y)
	w = np.dot(inverse, xy)
	return w

# Starts with an initial guess for w
# and performs gradient descent until it converges
def gradient_descent(X, Y, alpha=0.00001):
	w = np.zeros(X.shape[0])
	while(True):
		transform = np.dot(X.T, w)
		paren = np.subtract(Y, transform)
		mult = np.dot(X, paren)
		loss = np.subtract(w, mult)
		w = np.subtract(w, np.dot(alpha, loss))
		if np.linalg.norm(loss) <= 0.001:
			break
	return w


if __name__ == '__main__':
	if len(sys.argv) == 1:
		# Test if gradient descent was implemented properly
		w = np.random.normal(0,1,(10))
		X, Y = generate_data(100, w)
		w_exact = exact_solution(X, Y)
		w_solved = gradient_descent(X, Y)
		print(w_exact)
		print(w_solved)
		if np.max(abs(w_exact-w_solved)) < 0.01:
			print("Gradient descent working!")
		else:
			print("Gradient descent not working")

	else:
		# Extract the online_shares dataset
		fp = open(sys.argv[1], 'r')
		lines = fp.readlines()
		features = [st.strip() for st in lines[0].split(',')]
		features.pop() # Get rid of shares label
		data = np.genfromtxt(sys.argv[1], delimiter=',')

		X = data[1:, :data.shape[1]-1].T
		Y = data[1:, data.shape[1]-1]

		xmeans = np.mean(X, axis=0)
		ymean = np.mean(Y)
		xstdevs = np.std(X,axis=0)
		ystdev = np.std(Y)

		# Normalize the data for numerical stability
		X_normalized = (X-xmeans)/xstdevs
		Y_normalized = (Y-ymean)/ystdev

		w_exact = exact_solution(X_normalized, Y_normalized)

		y_pred = ystdev*np.dot(X_normalized.T, w_exact)+ymean

		rmse = np.linalg.norm(Y-y_pred)/np.sqrt(len(Y))
		print("Root mean squared error = ", rmse)
		print("Standard deviation", np.std(Y))
		print("Normed stddev", np.std(Y)/ymean)
		print('Normed rmse = ', rmse/ymean)

		# Sort descending by absolute value of weights
		sorted_inds = np.argsort(abs(w_exact))[::-1]

		# Print out weights
		for i in range(len(w_exact)):
			print(w_exact[sorted_inds[i]], ',', features[sorted_inds[i]])


