import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import sys

sys.path.append("./")
from common_utils.train_utils import Encoder, pickle_model


def train(msg):
    random.seed(0)
    training_data_uri = msg.payload.get("$ref", "./data/customer_churn-prepped.csv")
    save_model_as = msg.payload.get("model_name")

    data = pd.read_csv(training_data_uri)
    feature_names = list(data.columns[:-1])

    # separate outcome
    y = data["Exited"]
    X = data.drop("Exited", axis=1)

    # apply category encoder
    scaler = Encoder(X)
    scaler.fit(X)

    X_onehot = scaler.transform(X)

    # split test and training
    X_train, X_test, y_train, y_test = train_test_split(X_onehot, y, random_state=0)

    # start model training
    rfMod = RandomForestClassifier(n_estimators=10, criterion="gini")
    rfMod.fit(X_train, y_train)
    # Compute the model accuracy on the given test data and labels
    rf_acc = rfMod.score(X_test, y_test)

    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(rfMod, scaler, "GBM", rf_acc, "Gradient Boosting Model", model_binary)
    print(rf_acc)
    return f"model: {model_binary}"

