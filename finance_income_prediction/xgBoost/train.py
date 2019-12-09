import random
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from finance_income_prediction.common_utils.train_utils import Encoder
from utils.encode_decode import pickle_model


def train(msg):
    random.seed(0)
    np.random.seed(0)
    training_data_uri = msg.payload.get("$ref", "./data/adult_income-prepped.csv")
    save_model_as = msg.payload.get('model_name')
    df = pd.read_csv(training_data_uri)

    # Separate outcome
    y = df["income"]
    X = df.drop("income", axis=1)

    # apply encoding to dataset
    scaler = Encoder(X)
    scaler.fit(X)

    X_onehot = scaler.transform(X)

    # split test and training
    X_train, X_test, y_train, y_test = train_test_split(
        X_onehot, y, test_size=0.25, random_state=4
    )

    # start model training
    xgbt = xgb.XGBClassifier(objective="binary:logistic", random_state=42)
    xgbt.fit(X_train, y_train)
    y_pred = xgbt.predict(X_test)
    predictions = [round(value) for value in y_pred]
    # evaluate predictions
    xgbt_acc = accuracy_score(y_test, predictions)
    model_binary = f'models/{save_model_as}.pkl'
    pickle_model(
        xgbt,
        scaler,
        "XGBoost",
        xgbt_acc,
        "Extreme Gradient Boosting Classifier",
        model_binary
    )
    print(xgbt_acc)
    return (f'model: {model_binary}')

