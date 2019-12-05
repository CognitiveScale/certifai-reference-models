import random
from sklearn.model_selection import train_test_split
from sklearn import svm
import pandas as pd
import sys
from utils.encode_decode import pickle_model
from bank_marketing.common_utils.train_utils import Encoder


def train(msg):
    random.seed(0)
    training_data_uri = msg.payload.get("$ref", "./data/bank_marketing-prepped.csv")
    save_model_as = msg.payload.get("model_name")
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
    SVM = svm.SVC(gamma="scale")
    SVM.fit(X_train.values, y_train.values)
    svm_acc = SVM.score(X_test.values, y_test.values)
    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(SVM, scaler, "SVM", svm_acc, "Support Vector Machine", model_binary)
    print(svm_acc)
    return f"model: {model_binary}"

