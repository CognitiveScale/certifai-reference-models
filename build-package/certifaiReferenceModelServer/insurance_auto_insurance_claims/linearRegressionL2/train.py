""" 
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""
from cortex import Cortex, Message
import json
import sys
import random
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
from certifaiReferenceModelServer.insurance_auto_insurance_claims.common_utils.train_utils import CategoricalEncoder
from certifaiReferenceModelServer.utils.encode_decode import pickle_model

RANDOM_SEED = 0


def train(msg):
    # for reproducible training
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    training_data_uri = msg.payload.get(
        "$ref", "./data/auto_insurance_claims_dataset.csv"
    )
    save_model_as = msg.payload.get("model_name")

    data = pd.read_csv(training_data_uri)
    train_dataset = training_data_uri.replace(".csv", "-train.csv")
    test_dataset = training_data_uri.replace(".csv", "-test.csv")
    train_data = pd.read_csv(train_dataset)
    test_data = pd.read_csv(test_dataset)

    # Separate outcome
    y = data["Total Claim Amount"]
    X = data.drop("Total Claim Amount", axis=1)

    y_train_df = train_data["Total Claim Amount"]
    X_train_df = train_data.drop("Total Claim Amount", axis=1)

    y_test_df = test_data["Total Claim Amount"]
    X_test_df = test_data.drop("Total Claim Amount", axis=1)

    # create encoder on entire dataset
    scaler = CategoricalEncoder()
    scaler.fit(X)

    # apply encoding to train and test data features
    # applied on test data to calculate accuracy metric
    X_train = scaler.transform(X_train_df)
    y_train = y_train_df

    X_test = scaler.transform(X_test_df)
    y_test = y_test_df

    # start model training
    lmodel_l2 = Ridge(
        alpha=0.1,
        copy_X=True,
        fit_intercept=True,
        max_iter=1000,
        normalize=False,
        random_state=RANDOM_SEED,
        tol=0.0001,
    )
    lmodel_l2.fit(X_train, y_train)
    y_pred = lmodel_l2.predict(X_test)
    l2_err = ((y_test - y_pred) ** 2).sum()  # Prediction error

    err = r2_score(y_test, y_pred)

    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(
        lmodel_l2,
        scaler,
        "Linear L2",
        err,
        "Linear regression with L2 regularization",
        model_binary,
    )
    print(err)
    return f"model: {model_binary}"


if __name__ == "__main__":
    print(train(Message(json.loads(sys.argv[1]))))
