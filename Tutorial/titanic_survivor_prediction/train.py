import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import random

RANDOM_SEED = 0
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

std_scaler = StandardScaler()


def load_data():
    titanic = sns.load_dataset('titanic')
    return titanic


def encoder(titanic):
    labelencoder = LabelEncoder()
    # Encode sex column
    titanic.iloc[:, 2] = labelencoder.fit_transform(titanic.iloc[:, 2].values)
    # Encode embarked
    titanic.iloc[:, 7] = labelencoder.fit_transform(titanic.iloc[:, 7].values)
    return titanic


def preprocess_data(titanic):
    # Drop / remove the columns
    titanic = titanic.drop(['deck', 'embark_town', 'alive', 'class', 'alone', 'adult_male', 'who'], axis=1)
    # Drop/remove the rows with missing values
    titanic = titanic.dropna(subset=['embarked', 'age'])
    return titanic


def split_data(titanic):
    global std_scaler
    titanic.to_csv('encoded_dataset.csv', index=False)
    X = titanic.iloc[:, 1:8].values
    Y = titanic.iloc[:, 0].values
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=RANDOM_SEED)
    X_train = std_scaler.fit_transform(X_train)
    X_test = std_scaler.transform(X_test)

    return X_train, X_test, Y_train, Y_test


def train_model():
    X_train, X_test, Y_train, Y_test = split_data(encoder(preprocess_data(load_data())))
    forest = RandomForestClassifier(n_estimators=10, criterion='entropy', random_state=0)
    forest.fit(X_train, Y_train)
    print(f'Random Forest Classifier Training Accuracy: {forest.score(X_train, Y_train)}')
    return forest, std_scaler
