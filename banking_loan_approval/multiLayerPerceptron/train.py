import random
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
import os
import sys
sys.path.append("./")
from common_utils.train_utils import Encoder, pickle_model


def train(msg):
    random.seed(0)
    training_data_uri = msg.payload.get("$ref", "./data/german_credit-decoded.csv")
    save_model_as = msg.payload.get('model_name')
    df = pd.read_csv(training_data_uri)
    # Separate outcome
    y = df["outcome"]
    X = df.drop("outcome", axis=1)

    # apply encoding to dataset
    scaler = Encoder()
    scaler.fit(X)

    X_onehot = scaler.transform(X)

    # split test and training
    X_train, X_test, y_train, y_test = train_test_split(
        X_onehot, y, test_size=0.25, random_state=0
    )

    # start model training
    mlp = MLPClassifier(hidden_layer_sizes=(20,20),max_iter=2000)
    mlp.fit(X_train.values, y_train.values)
    mlp_acc = mlp.score(X_test.values,y_test.values)
    model_binary = f'models/{save_model_as}.pkl'
    pickle_model(
        mlp,
        scaler,
        "MLP",
        mlp_acc,
        "Basic MLP model",
        model_binary,
    )
    print(mlp_acc)
    return (f'model: {model_binary}')

