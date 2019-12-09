import pickle
import random
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
from bank_marketing.common_utils.train_utils import Encoder
from utils.encode_decode import pickle_model


def train(msg):
    random.seed(0)
    training_data_uri = msg.payload.get("$ref", "./data/bank_marketing-prepped.csv")
    save_model_as = msg.payload.get("model_name")
    print(msg.payload)
    data = pd.read_csv(training_data_uri)
    feature_names = list(data.columns[:-1])

    # Separate outcome
    y = data["deposit"]
    X = data.drop("deposit", axis=1)

    # apply encoder data
    scaler = Encoder(X)
    scaler.fit(X)

    X_onehot = scaler.transform(X)

    # split test and training
    X_train, X_test, y_train, y_test = train_test_split(
        X_onehot, y, test_size=0.3, random_state=4
    )
    # start model training
    logit = LogisticRegression(random_state=0, solver="lbfgs")
    logit.fit(X_train.values, y_train.values)
    logit_acc = logit.score(X_test.values, y_test.values)
    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(
        logit, scaler, "LR", logit_acc, "Logistic Regression Classifier", model_binary
    )
    print(logit_acc)
    return f"model: {model_binary}"

