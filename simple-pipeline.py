import pandas as pd 
import numpy as np 
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

winedf = pd.read_csv('Data/winequality/winequality-red.csv', delimiter = ';')
# print(winedf.isnull().sum())

X = winedf.drop('quality', axis=1)
y = winedf['quality']

X_train, X_test, y_train, y_test  = train_test_split(X, y, test_size = .3, random_state = 30, stratify = y)

steps = [('scaler', StandardScaler()), ('SVM', SVC())]
pipeline = Pipeline(steps)

parameters = {'SVM__C' : [.001, .1, 1, 10, 100, 10.5], 'SVM__gamma': [.1, 0, .01]}
grid = GridSearchCV(pipeline, param_grid = parameters)

grid.fit(X_train, y_train)
print("score = 3.2%f" % (grid.score(X_test, y_test)))

# What I learned here

# A pipeline is a essentially a streamlined way of defining a set of steps 
# to be undertaken by a model. The way sklearn is set up, these pipelines 
# consists of ordered pairs where the first entry is a name and the second a 
# transformation or estimator. Sklearn requires that the list end with an 
# estimator. 

# Grid Search also makes a lot more sense to me than it did the first time I 
# encountered it. We create a dictionary whose keys are parameters and whose 
# values are lists of values those parameters can take. Then, gridsearch does
# an exhaustive search over the spaces we've delimited, looking for optima.
# sklearn conveniently makes it so that we can standard methods like .score() 
# and .fit() directly from our gridsearch object. 