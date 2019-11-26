import random
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import sys

sys.path.append("./")
from common_utils.train_utils import Encoder, pickle_model


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
    dtree = DecisionTreeClassifier(criterion='entropy', random_state=0)
    dtree.fit(X_train.values, y_train.values)
    dtree_acc = dtree.score(X_test.values, y_test.values)
    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(
        dtree, scaler, "Decision Tree", dtree_acc, "Decision Tree Classifier", model_binary
    )
    print(dtree_acc)
    return f"model: {model_binary}"

