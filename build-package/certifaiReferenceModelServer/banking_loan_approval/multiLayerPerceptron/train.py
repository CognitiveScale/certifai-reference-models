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
from certifaiReferenceModelServer.banking_loan_approval.common_utils.train_utils import Encoder
from certifaiReferenceModelServer.utils.encode_decode import pickle_model

RANDOM_SEED = 0


def train(msg):
    # for reproducible training
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    training_data_uri = msg.payload.get("$ref", "./data/german_credit-decoded.csv")
    save_model_as = msg.payload.get("model_name")

    data = pd.read_csv(training_data_uri)
    train_dataset = training_data_uri.replace(".csv", "-train.csv")
    test_dataset = training_data_uri.replace(".csv", "-test.csv")
    train_data = pd.read_csv(train_dataset)
    test_data = pd.read_csv(test_dataset)

    # Separate outcome
    y = data["outcome"]
    X = data.drop("outcome", axis=1)

    y_train_df = train_data["outcome"]
    X_train_df = train_data.drop("outcome", axis=1)

    y_test_df = test_data["outcome"]
    X_test_df = test_data.drop("outcome", axis=1)

    # create encoder on entire dataset
    scaler = Encoder()
    scaler.fit(X)

    # apply encoding to train and test data features
    # applied on test data to calculate accuracy metric
    X_train = scaler.transform(X_train_df)
    y_train = y_train_df

    X_test = scaler.transform(X_test_df)
    y_test = y_test_df

    # start model training
    mlp = MLPClassifier(
        hidden_layer_sizes=(20, 20), max_iter=2000, random_state=RANDOM_SEED
    )
    mlp.fit(X_train.values, y_train.values)
    mlp_acc = mlp.score(X_test.values, y_test.values)
    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(mlp, scaler, "MLP", mlp_acc, "Basic MLP model", model_binary)
    print(mlp_acc)
    return f"model: {model_binary}"

if __name__ == "__main__":
    print(train(Message(json.loads(sys.argv[1]))))