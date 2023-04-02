# import libraries
import pandas as pd
import numpy as np
import logging
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# Logging config
FORMAT = '%(asctime)s | %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

logging.info('Reading cleaned data from csv file...')
df_cleaned = pd.read_csv('build/data/data_cleaned.csv')

logging.info('Creating power transforms of mass, bmi and exercise...')
df_cleaned["mass_square"] = df_cleaned['mass']**2
df_cleaned["bmi_square"] = df_cleaned['bmi']**2
df_cleaned["exercise_sqrt"] = np.power(df_cleaned['exercise'], 1/2)

logging.info('Removing mass from feature list...')
logging.info('Separating features in X and lifespan in y...')
X = df_cleaned.iloc[:, df_cleaned.columns.isin(['genetic', 'length', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'mass_square', 'bmi_square', 'exercise_sqrt'])]
y = df_cleaned['lifespan']

logging.info('Splitting data in train and test data...')
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

logging.info('Building model...')
pipe = Pipeline([('model', LinearRegression())])
# The pipeline can be used as any other estimator
# and avoids leaking the test set into the train set
logging.info('Fitting model with train data...')
pipe.fit(X_train, y_train)

logging.info('Pickle trained model...')
filename = 'build/data/finalized_model.pkl'
logging.info('Saved pickled model to "finalized_model.pkl"...')
pickle.dump(pipe, open(filename, 'wb'))
