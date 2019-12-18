import random
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import sys
from bank_marketing.common_utils.train_utils import Encoder
from utils.encode_decode import pickle_model


def train(msg):
    training_data_uri = msg.payload.get("$ref", "./data/bank_marketing-prepped.csv")
    save_model_as = msg.payload.get("model_name")

    data = pd.read_csv(training_data_uri)
    train_dataset = training_data_uri.replace(".csv", "-train.csv")
    test_dataset = training_data_uri.replace(".csv", "-test.csv")
    train_data = pd.read_csv(train_dataset)
    test_data = pd.read_csv(test_dataset)

    # Separate outcome
    y = data["deposit"]
    X = data.drop("deposit", axis=1)

    y_train_df = train_data["deposit"]
    X_train_df = train_data.drop("deposit", axis=1)

    y_test_df = test_dataset["deposit"]
    X_test_df = test_dataset.drop("deposit", axis=1)

    # create encoder on entire dataset
    scaler = Encoder(X)
    scaler.fit(X)

    # apply encoding to train and test data features
    X_train = scaler.transform(X_train_df)
    y_train = y_train_df

    X_test = scaler.transform(X_test_df)
    y_test = y_test_df

    # start model training
    dtree = DecisionTreeClassifier(criterion="entropy", random_state=0)
    dtree.fit(X_train.values, y_train.values)

    dtree_acc = dtree.score(X_test.values, y_test.values)
    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(
        dtree,
        scaler,
        "Decision Tree",
        dtree_acc,
        "Decision Tree Classifier",
        model_binary,
    )
    print(dtree_acc)
    return f"model: {model_binary}"

