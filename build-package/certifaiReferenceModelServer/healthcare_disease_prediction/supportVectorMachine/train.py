""" 
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""

import json
import sys
import random
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from certifaiReferenceModelServer.healthcare_disease_prediction.common_utils.train_utils import \
    prep_diabetes_dataset, WrappedStandardScaler
from certifaiReferenceModelServer.utils.encode_decode import pickle_model

RANDOM_SEED = 0


def train(msg):
    # for reproducible training
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    training_data_uri = msg.get('payload', {}).get("$ref", "./data/diabetes.csv")
    save_model_as = msg.get('payload', {}).get("model_name")

    data = prep_diabetes_dataset(pd.read_csv(training_data_uri))
    train_dataset = training_data_uri.replace(".csv", "-train.csv")
    test_dataset = training_data_uri.replace(".csv", "-test.csv")
    train_data = prep_diabetes_dataset(pd.read_csv(train_dataset))
    test_data = prep_diabetes_dataset(pd.read_csv(test_dataset))

    # Separate outcome
    y = data["Outcome"]
    X = data.drop("Outcome", axis=1)

    y_train_df = train_data["Outcome"]
    X_train_df = train_data.drop("Outcome", axis=1)

    y_test_df = test_data["Outcome"]
    X_test_df = test_data.drop("Outcome", axis=1)

    # create encoder on entire dataset
    scaler = WrappedStandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit(X)

    # apply encoding to train and test data features
    # applied on test data to calculate accuracy metric
    X_train = scaler.transform(X_train_df)
    y_train = y_train_df

    X_test = scaler.transform(X_test_df)
    y_test = y_test_df

    # start model training
    SVM = svm.SVC(gamma="scale", random_state=RANDOM_SEED)
    SVM.fit(X_train, y_train)
    SVM.score(X_test, y_test)
    svm_acc = SVM.score(X_test, y_test)

    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(SVM, scaler, "SVM", svm_acc, "Basic SVM model", model_binary)
    print(svm_acc)
    return f"model: {model_binary}"


if __name__ == "__main__":
    print(train(json.loads(sys.argv[1])))
