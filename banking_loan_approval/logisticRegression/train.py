import random
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from banking_loan_approval.common_utils.train_utils import Encoder
from utils.encode_decode import pickle_model


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
    logit = LogisticRegression(random_state=0, solver="lbfgs", max_iter=1000)
    logit.fit(X_train.values, y_train.values)
    logit_acc = logit.score(X_test.values, y_test.values)
    model_binary = f'models/{save_model_as}.pkl'
    pickle_model(
        logit,
        scaler,
        "LR",
        logit_acc,
        "Logistic Regression Classifier",
        model_binary,
    )
    print(logit_acc)
    return (f'model: {model_binary}')
