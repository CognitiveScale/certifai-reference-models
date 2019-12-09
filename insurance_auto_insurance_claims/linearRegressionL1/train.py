import random
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score
import pandas as pd
from insurance_auto_insurance_claims.common_utils.train_utils import CategoricalEncoder
from utils.encode_decode import pickle_model


def train(msg):
    random.seed(0)
    training_data_uri = msg.payload.get(
        "$ref", "./data/auto_insurance_claims_dataset.csv"
    )
    save_model_as = msg.payload.get("model_name")
    data = pd.read_csv(training_data_uri)

    # Getting feature names
    feature_names = list(data.columns)
    feature_names.remove("Total Claim Amount")

    # Train-test split
    X = data.copy()
    y = X["Total Claim Amount"]
    X_tr, X_tst, y_tr, y_tst = train_test_split(X, y, test_size=1000, random_state=0)

    # Tranforming train and test data
    scaler = CategoricalEncoder()
    scaler.fit(X_tr)
    X_train = scaler.transform(X_tr.drop(["Total Claim Amount"], axis=1))
    y_train = X_tr["Total Claim Amount"]

    X_test = scaler.transform(X_tst.drop(["Total Claim Amount"], axis=1))
    y_test = X_tst["Total Claim Amount"]

    # start model training
    lmodel_l1 = Lasso(
        alpha=1e-4,
        copy_X=True,
        fit_intercept=True,
        max_iter=1000,
        normalize=False,
        positive=False,
        precompute=False,
        random_state=None,
        selection="cyclic",
        tol=0.0001,
        warm_start=False,
    )
    lmodel_l1.fit(X_train, y_train)
    y_pred = lmodel_l1.predict(X_test)
    l1_err = ((y_test - y_pred) ** 2).sum()  # Prediction error

    err = r2_score(y_test, y_pred)

    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(
        lmodel_l1,
        scaler,
        "Linear L1",
        err,
        "Linear regression with L1 regularization",
        model_binary,
    )
    print(err)
    return f"model: {model_binary}"

