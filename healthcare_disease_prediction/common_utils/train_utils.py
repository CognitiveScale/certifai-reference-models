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

