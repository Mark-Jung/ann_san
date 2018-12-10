import numpy as np
import csv, random
import math
# polynomial regression
'''
1. read in train and test csv
2. create matrix from train and test
3. calculate the weight vector from the training matrix
4. test on test matrix
5. compare the prediction vector with the actual vector
6. print accuracy
'''

def parse(filename):
	'''
	reads in csv
	'''
	out = []
	file = open(filename,'r')
	filetoread = csv.reader(file)

	header = next(filetoread)

	for row in filetoread:
		out.append(dict(zip(header, row)))
		
	return out

def fill_attribute_vectors(examples, attributes, attr_names, popularity):
	'''
	input: list of examples, list of attribute lists, list of attribute names in strings, and the list of popularity
	output: does not return anything.
	what it does: fills in attribute lists and popularity list from the examples
	'''
	for example in examples:
		for ind, attr in enumerate(attr_names):
			attributes[ind].append(example[attr])
		popularity.append(example['popularity_num'])

def get_matrix_X_aug_y(examples):
	'''
	input: list of examples
	output: a matrix X augmented by vector y
	'''
	popularity = []
	popularity_num = []

	key = []
	mode = []
	time_signature = []
	acousticness = []
	danceablility = []
	energy = []
	instrumentalness = []
	liveness = []
	loudness = []
	speechiness = []
	valence = []
	tempo = []
	artist_followers = []
	artist_popularity = []

	attributes = [mode, key, artist_followers, artist_popularity, time_signature, acousticness, danceablility, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo]
	attr_names = ['mode', 'key', 'artist_followers', 'artist_popularity', 'time_signature', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'valence', 'tempo']
	fill_attribute_vectors(examples, attributes, attr_names, popularity)

	mtrx_x = []
	for i in range(len(examples)):
		tmp = []
		for ind, att in enumerate(attributes):
			# linear regression
			tmp.append(float(att[i]))
			# polynomial regression
			#tmp.append(pow(float(att[i]),ind+1))
		tmp.append(float(popularity[i]))
		mtrx_x.append(tmp)
	return np.matrix(mtrx_x)

def remove_aug(mtrx):
	'''
	input: augmented matrix X|y
	output: matrix X and vector y
	'''
	mtrx_x = []
	vec_y = []

	for i in range(len(mtrx)):
		temp = []
		for j in (mtrx[i].A1)[:-1]:
			temp.append(j)
		mtrx_x.append(temp)
		vec_y.append([(mtrx[i].A1)[-1]])

	return np.matrix(mtrx_x), np.matrix(vec_y)

def calculate_weight_vector(mtrx_x, pop_vec):
	'''
	input: matrix X and vector y
	output: the weight vector w, or an empty list if the matrix is not invertible

	using regression equation
	w = (Xt X)^-1 Xt y
	'''
	try:
		xttx_inv = np.linalg.inv(np.matmul(mtrx_x.T, mtrx_x))
	except np.linalg.LinAlgError:
		print('singular matrix')
		return []
	else:
		xttx_inv_t_xt = np.matmul(xttx_inv, mtrx_x.T)

		weight_vec = np.matmul(xttx_inv_t_xt, pop_vec)
		return weight_vec

def test_on_vector(vec, test_x, test_y):
	'''
	input: weight vector w, X matrix of the test set, y vector of the test set
	output: the error vector and the percentage of accuracy

	success if the error is less than 5
	prediction above 100 and below 0 is fixed to 100 and 0, respectively
	'''
	prediction = np.matmul(test_x, vec)
	result = []
	correct = 0
	for ind, a in enumerate(prediction):
		pred_i = test_y[ind][0]
		if(pred_i > 100):
			pred_i = 100
		if(pred_i < 0):
			pred_i = 0
		val = a[0] - test_y[ind][0]

		if(val < 10 and val > -10):
			correct += 1
		result.append(val)
	percent = correct*100/len(test_y)
	return result, percent

def main():
	examples = parse('train.csv')
	print('there are {} examples'.format(len(examples)))

	accuracies = []
	haha = np.zeros((14,1))

	for i in range(10):

		random.shuffle(examples,random.random)

		mtrx_train = get_matrix_X_aug_y(examples[:len(examples)//10])
		mtrx_test = get_matrix_X_aug_y(examples[len(examples)//10:])

		accuracy = []
		
		mtrx_x, y = remove_aug(mtrx_train)
		vec = calculate_weight_vector(mtrx_x, y)
		haha = haha + vec
		test_x, test_y = remove_aug(mtrx_test)
		vec2, percent = test_on_vector(vec, test_x, test_y)

		accuracies.append(percent)
		print(percent)

	print('the average of weight vectors are\n',vec/10)
	print('average accuracy is {}'.format(sum(accuracies)/10))

if __name__ == '__main__':
	main()