import os

RANDOM_SEED = 0
os.environ["PYTHONHASHSEED"] = str(RANDOM_SEED)

import random
import numpy as np
from tensorflow import set_random_seed
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import r2_score
import pandas as pd
from insurance_auto_insurance_claims.common_utils.train_utils import (
    CategoricalEncoder,
    NNPredictWrapper,
)
from utils.encode_decode import pickle_model


def train(msg):
    # for reproducible training
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    set_random_seed(RANDOM_SEED)

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
    NN = Sequential()
    NN.add(Dense(1000, input_dim=X_train.shape[1], activation="relu"))
    NN.add(Dense(200, activation="relu"))
    NN.add(Dense(50, activation="relu"))
    NN.add(Dense(1))
    NN.summary()

    NN.compile(loss="mse", optimizer="adam", metrics=["mse", "mae"])
    NN.fit(X_train, y_train, epochs=500, batch_size=300, verbose=0)

    y_pred = NN.predict(X_test)
    err = r2_score(y_test, y_pred)

    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(
        NNPredictWrapper(NN),
        scaler,
        "Neural Network",
        err,
        "Four-layer neural network",
        model_binary,
    )
    print(err)
    return f"model: {model_binary}"

