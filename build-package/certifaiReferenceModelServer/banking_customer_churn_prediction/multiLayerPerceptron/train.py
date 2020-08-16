""" 
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""
from cortex import Cortex, Message
import json
import sys
import random
from sklearn.neural_network import MLPClassifier
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
    mlp = MLPClassifier(random_state=RANDOM_SEED)
    mlp.fit(X_train, y_train)
    mlp.score(X_test, y_test)
    mlp_acc = mlp.score(X_test, y_test)
    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(mlp, scaler, "MLP", mlp_acc, "Basic MLP classifier", model_binary)
    print(mlp_acc)
    return f"model: {model_binary}"

if __name__ == "__main__":
    print(train(Message(json.loads(sys.argv[1]))))