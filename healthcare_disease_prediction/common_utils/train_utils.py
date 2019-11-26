from sklearn import preprocessing
import pandas as pd
import pickle
import time
from sklearn.model_selection import train_test_split
from sklearn import preprocessing


def prep_diabetes_dataset(dataset_path):  # we assume a pre-cleaned dataset
    # dataset_path =f"data/diabetes.csv"
    with open(dataset_path, "rb") as fl:
        data = pd.read_csv(dataset_path)
    data = data[(data.BloodPressure != 0) & (data.BMI != 0) & (data.Glucose != 0)]
    y = data["Outcome"]
    X = data.drop("Outcome", axis=1)
    return train_test_split(X, y, random_state=0)


def pkl_path(project, model):
    return "models/{}_{}.pkl".format(project, model)


def pickle_model(model, scaler, model_name, test_accuracy, description, filename):
    model_obj = {}
    model_obj["model"] = model
    model_obj["scaler"] = scaler
    model_obj["modelName"] = model_name
    model_obj["modelDescription"] = description
    model_obj["test_acc"] = test_accuracy
    model_obj["createdTime"] = int(time.time())
    with open(filename, "wb") as file:
        pickle.dump(model_obj, file)
    print(f"Saved: {model_name}")
