import random
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import os
import sys
from sklearn.ensemble import RandomForestClassifier

sys.path.append("./")
from common_utils.train_utils import Encoder, pickle_model, pkl_path


def train(msg):
    random.seed(0)
    np.random.seed(0)
    training_data_uri = msg.payload.get("$ref", "./data/adult_income-prepped.csv")
    save_model_as = msg.payload.get('model_name')
    df = pd.read_csv(training_data_uri)

    feature_names = list(df.columns[:-1])

    # Separate outcome
    y = df["income"]
    X = df.drop("income", axis=1)

    # apply encoding to dataset
    scaler = Encoder(X)
    scaler.fit(X)

    X_onehot = scaler.transform(X)

    # split test and training
    X_train, X_test, y_train, y_test = train_test_split(
        X_onehot, y, test_size=0.25, random_state=4
    )

    # start model training
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    rf_acc = rf.score(X_test, y_test)
    model_binary = f'models/{save_model_as}.pkl'
    pickle_model(rf, scaler, "RF", rf_acc, "Random Forest Classifier", model_binary)
    print(rf_acc)
    return (f'model: {model_binary}')
