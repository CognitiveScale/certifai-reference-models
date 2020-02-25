from cortex import Cortex, Message
import json
import sys
import random
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import numpy as np
from certifaiReferenceModelServer.banking_customer_churn_prediction.common_utils.train_utils import Encoder
from certifaiReferenceModelServer.utils.encode_decode import pickle_model

RANDOM_SEED = 0


def train(msg):
    # for reproducible training
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    training_data_uri = msg.payload.get("$ref", "./data/customer_churn-prepped.csv")
    save_model_as = msg.payload.get("model_name")

    data = pd.read_csv(training_data_uri)
    train_dataset = training_data_uri.replace(".csv", "-train.csv")
    test_dataset = training_data_uri.replace(".csv", "-test.csv")
    train_data = pd.read_csv(train_dataset)
    test_data = pd.read_csv(test_dataset)

    # Separate outcome
    y = data["Exited"]
    X = data.drop("Exited", axis=1)

    y_train_df = train_data["Exited"]
    X_train_df = train_data.drop("Exited", axis=1)

    y_test_df = test_data["Exited"]
    X_test_df = test_data.drop("Exited", axis=1)

    # create encoder on entire dataset
    scaler = Encoder(X)
    scaler.fit(X)

    # apply encoding to train and test data features
    # applied on test data to calculate accuracy metric
    X_train = scaler.transform(X_train_df)
    y_train = y_train_df

    X_test = scaler.transform(X_test_df)
    y_test = y_test_df

    # start model training
    gbMod = GradientBoostingClassifier(
        loss="deviance", n_estimators=200, random_state=RANDOM_SEED
    )
    gbMod.fit(X_train, y_train)

    gb_acc = gbMod.score(X_test, y_test)

    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(gbMod, scaler, "GBM", gb_acc, "Gradient Boosting Model", model_binary)
    print(gb_acc)
    return f"model: {model_binary}"

if __name__ == "__main__":
    print(train(Message(json.loads(sys.argv[1]))))