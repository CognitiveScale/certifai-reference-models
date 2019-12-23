import random
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np
from finance_income_prediction.common_utils.train_utils import Encoder
from utils.encode_decode import pickle_model

RANDOM_SEED = 0


def train(msg):
    # for reproducible training
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    training_data_uri = msg.payload.get("$ref", "./data/adult_income-prepped.csv")
    save_model_as = msg.payload.get("model_name")

    data = pd.read_csv(training_data_uri)
    train_dataset = training_data_uri.replace(".csv", "-train.csv")
    test_dataset = training_data_uri.replace(".csv", "-test.csv")
    train_data = pd.read_csv(train_dataset)
    test_data = pd.read_csv(test_dataset)

    # Separate outcome
    y = data["income"]
    X = data.drop("income", axis=1)

    y_train_df = train_data["income"]
    X_train_df = train_data.drop("income", axis=1)

    y_test_df = test_data["income"]
    X_test_df = test_data.drop("income", axis=1)

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
    logit = LogisticRegression(random_state=RANDOM_SEED, solver="lbfgs", max_iter=1000)
    logit.fit(X_train.values, y_train.values)
    logit_acc = logit.score(X_test.values, y_test.values)
    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(
        logit, scaler, "LR", logit_acc, "Logistic Regression Classifier", model_binary
    )
    print(logit_acc)
    return f"model: {model_binary}"

