
import pandas as pd
from matplotlib import pyplot
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

"""def load_data(file_name):
	data = pd.read_csv(file_name, header=0, index_col=1, parse_dates=True, squeeze=True)
	return data"""

def plot_data(data):
	# determine the number of features
	n_features = data.values.shape[1]
	pyplot.figure()
	for i in range(1, n_features):
		pyplot.subplot(n_features, 1, i)
		pyplot.plot(data.index, data.values[:, i])
		pyplot.title(data.columns[i], y=0.5, loc='right')
	pyplot.show()


def naive_prediction(values):

	# split data into inputs and outputs
	X, y = values[:, :-1], values[:, -1]
	# split the dataset
	trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.3, shuffle=False, random_state=1)

	# evaluate skill of predicting each class value
	for value in [0, 1]:
		# forecast
		yhat = [value for x in range(len(testX))]
		# evaluate
		score = accuracy_score(testy, yhat)
		# summarize
		print('Naive=%d score=%.3f' % (value, score))


def logistic_regression(values):

	# split data into inputs and outputs
	X, y = values[:, :-1], values[:, -1]
	# split the dataset
	trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.3, shuffle=False, random_state=1)
	# define the model
	model = LogisticRegression()
	# fit the model on the training set
	model.fit(trainX, trainy)
	# predict the test set
	yhat = model.predict(testX)
	# evaluate model skill
	score = accuracy_score(testy, yhat)
	print(score)


def feature_selection_and_log_reg(values, data):

	# basic feature selection
	features = [0, 1, 2, 3, 4]
	for f in features:
		# split data into inputs and outputs
		X, y = values[:, f].reshape((len(values), 1)), values[:, -1]
		# split the dataset
		trainX, testX, trainy, testy = train_test_split(X, y, test_size=0.3, shuffle=False, random_state=1)
		# define the model
		model = LogisticRegression()
		# fit the model on the training set
		model.fit(trainX, trainy)
		# predict the test set
		yhat = model.predict(testX)
		# evaluate model skill
		score = accuracy_score(testy, yhat)
		print('feature=%d, name=%s, score=%.3f' % (f, data.columns[f], score))

def main():

	# load the dataset
	data = pd.read_csv('combined.csv', header=0, index_col=0, parse_dates=True, squeeze=True)
	plot_data(data)
	values = data.values
	
	#naive_prediction(values)
	#logistic_regression(values)
	feature_selection_and_log_reg(values, data)

  
if __name__== "__main__":
  main()