import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd

from banking_customer_churn_prediction.common_utils.train_utils import Encoder
from utils.encode_decode import pickle_model


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
    gbMod = GradientBoostingClassifier(loss="deviance", n_estimators=200)
    gbMod.fit(X_train, y_train)

    gb_acc = gbMod.score(X_test, y_test)

    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(gbMod, scaler, "GBM", gb_acc, "Gradient Boosting Model", model_binary)
    print(gb_acc)
    return f"model: {model_binary}"
