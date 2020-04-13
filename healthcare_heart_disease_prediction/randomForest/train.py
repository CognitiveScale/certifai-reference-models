import sys
import json
import random
import pandas as pd
import numpy as np
from cortex import Message
from sklearn.ensemble import RandomForestClassifier
from utils.encode_decode import pickle_model
from healthcare_heart_disease_prediction.common_utils.train_utils import CategoricalEncoder

RANDOM_SEED = 0

def train(msg):
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    training_data_uri = msg.payload.get("$ref", "./data/heart_disease_multiclass-prepped.csv")
    save_model_as = msg.payload.get("model_name")

    data = pd.read_csv(training_data_uri)
    train_dataset = training_data_uri.replace(".csv", "-train.csv")
    test_dataset = training_data_uri.replace(".csv", "-test.csv")
    train_data = pd.read_csv(train_dataset)
    test_data = pd.read_csv(test_dataset)

    # Separate outcome
    y = data["class_att"]
    X = data.drop("class_att", axis=1)

    y_train_df = train_data["class_att"]
    X_train_df = train_data.drop("class_att", axis=1)

    y_test_df = test_data["class_att"]
    X_test_df = test_data.drop("class_att", axis=1)

    # create encoder on entire dataset
    scaler = CategoricalEncoder(X)
    scaler.fit(X)

    # apply encoding to train and test data features
    # applied on test data to calculate accuracy metric
    X_train = scaler.transform(X_train_df)
    y_train = y_train_df

    X_test = scaler.transform(X_test_df)
    y_test = y_test_df

    # start model training
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    rf_acc = rf.score(X_test,y_test)
    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(rf, scaler, 'RF', rf_acc, 'Random Forest Classifier', model_binary)
    print(rf_acc)
    return f"model: {model_binary}"

if __name__ == "__main__":
    print(train(Message(json.loads(sys.argv[1]))))
