import random
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.metrics import r2_score
import pandas as pd
import sys

sys.path.append("./")
from common_utils.train_utils import CategoricalEncoder, NNPredictWrapper, pickle_model


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

