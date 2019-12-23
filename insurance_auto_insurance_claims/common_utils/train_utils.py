from sklearn import preprocessing
import pandas as pd
import pickle
import time
from sklearn import preprocessing
import sys
import numpy as np

class CategoricalEncoder:

    # Initialization
    def __init__(self):
        self.minmax_ = {}
        self.cat_dict = {}

    # One-hot encoding of each column
    def encodeColumn(self, oldCol, labels):
        encoder = preprocessing.OneHotEncoder()

        encoder.fit(np.unique(labels).reshape(-1, 1))

        to_transform = [[c.strip()] for c in oldCol]
        newCol = encoder.transform(to_transform)

        return newCol.toarray()

    def get_num_cat_index(self, df):
        # Returns numpy arrays of indices containing numerical and categorical data
        numeric_cols = []
        categorical_cols = []

        # get numerical columns from original data
        for idx, header in enumerate(df.columns):
            if isinstance(df.iloc[0, idx], (np.int, np.int64)) or isinstance(
                df.iloc[0, idx], (np.float, np.float64)
            ):
                numeric_cols.append(header)
            else:
                categorical_cols.append(header)
        return numeric_cols, categorical_cols

    def fit(self, X):
        # Learn transformation parameters from (training) data
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X, columns=COLUMNS)

        num_col, cat_col = self.get_num_cat_index(
            X
        )  # Determine which features are num/cat

        scale_params = {}  # Scaling params for numerical data
        for idx, header in enumerate(X):
            if header in num_col:  # Min-max scaling if numerical
                col_min = np.amin(X[header].values)
                col_max = np.amax(X[header].values)
                scale_params[header] = (col_min, col_max)

        self.minmax_ = scale_params
        return self

    def transform(self, X, target=False):
        # Function for preprocessing of read data
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X, columns=COLUMNS)

        num_col, cat_col = self.get_num_cat_index(
            X
        )  # Determine which features are num/cat

        col_idx = 0  # Index of column
        claims_dict = get_columns_dict()
        if not target:  # If target variable is present in input df
            del claims_dict["Total Claim Amount"]

        all_column_names = get_expanded_cols(X, claims_dict)
        num_rows = X.shape[0]
        trans_df = np.zeros((num_rows, len(all_column_names)))
        cur_col = 0

        for idx, header in enumerate(X):
            if header in cat_col:  # One-hot encoding if categorical
                encoded_col = self.encodeColumn(X[header], claims_dict[header])
                # print(encoded_col.shape)
                len_col = len(claims_dict[header])
                encoded_col = encoded_col.reshape((X.shape[0], len_col))
                self.cat_dict[header] = np.linspace(
                    col_idx, col_idx + len_col - 1, len_col, dtype=np.int16
                )
                col_idx = col_idx + len_col

            if header in num_col:  # Min-max scaling if numerical
                min_val = self.minmax_[header][0]
                max_val = self.minmax_[header][1]
                if max_val == min_val:
                    max_val += 1e-7
                encoded_col = (X[header].values - min_val) / (max_val - min_val)
                if header != "Total Claim Amount":
                    col_idx = col_idx + 1

            encoded_col = encoded_col.reshape((num_rows, -1))
            end_col = cur_col + np.size(encoded_col, 1)
            # print('header', header)
            # print(f'{cur_col} --> {end_col}... shape {trans_df.shape}')
            trans_df[:, cur_col:end_col] = encoded_col
            cur_col = end_col

        return pd.DataFrame(trans_df, columns=all_column_names)

    def inverse_transform(self, X):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X, columns=COLUMNS)

        columns_dict = get_columns_dict()
        del columns_dict["Total Claim Amount"]
        all_pds = []

        ohe_col_start_idx = 0
        for col_name, categories in columns_dict.items():
            num_categories = len(categories)
            if num_categories == 1:  # Numeric
                min_val, max_val = self.minmax_[col_name]
                unnorm_values = X.iloc[:, ohe_col_start_idx].apply(
                    lambda x: x * (max_val - min_val) + min_val
                )
                new_df = unnorm_values.to_frame(col_name)
                ohe_col_start_idx += 1
            else:
                ohe_col_end_idx = ohe_col_start_idx + num_categories
                ohe_data = X.iloc[:, ohe_col_start_idx:ohe_col_end_idx]
                original_space = ohe_data.idxmax(1) - ohe_col_start_idx
                original_space = original_space.apply(lambda x: categories[x])
                new_df = original_space.to_frame(col_name)
                ohe_col_start_idx = ohe_col_end_idx

            all_pds.append(new_df)

        return pd.concat(all_pds, axis=1)


# TODO  (CMA): get columns to be passed from HostedModel?
COLUMNS = [
    "State Code",
    "Claim Amount",
    "Coverage",
    "Education",
    "EmploymentStatus",
    "Gender",
    "Income",
    "Location Code",
    "Marital Status",
    "Monthly Premium Auto",
    "Months Since Last Claim",
    "Months Since Policy Inception",
    "Number of Open Complaints",
    "Number of Policies",
    "Policy",
    "Claim Reason",
    "Sales Channel",
    "Vehicle Class",
    "Vehicle Size",
]  # "Total Claim Amount"


def get_columns_dict():
    claims_dict = {
        "State Code": ["KS", "NE", "OK", "MO", "IA"],
        "Claim Amount": ["Amount"],
        "Coverage": ["Basic", "Extended", "Premium"],
        "Education": [
            "High School or Below",
            "College",
            "Bachelor",
            "Master",
            "Doctor",
        ],
        "EmploymentStatus": [
            "Unemployed",
            "Employed",
            "Medical Leave",
            "Disabled",
            "Retired",
        ],
        "Gender": ["M", "F"],
        "Income": ["Amount"],
        "Location Code": ["Suburban", "Rural", "Urban"],
        "Marital Status": ["Married", "Single", "Divorced"],
        "Monthly Premium Auto": ["Amount"],
        "Months Since Last Claim": ["Months"],
        "Months Since Policy Inception": ["Months"],
        "Number of Open Complaints": ["Number"],
        "Number of Policies": ["Number"],
        "Policy": [
            "Corporate L1",
            "Corporate L2",
            "Corporate L3",
            "Personal L1",
            "Personal L2",
            "Personal L3",
            "Special L1",
            "Special L2",
            "Special L3",
        ],
        "Claim Reason": ["Collision", "Scratch/Dent", "Hail", "Other"],
        "Sales Channel": ["Agent", "Web", "Call Center", "Branch"],
        "Total Claim Amount": ["Amount"],
        "Vehicle Class": [
            "Two-Door Car",
            "Four-Door Car",
            "SUV",
            "Luxury SUV",
            "Sports Car",
            "Luxury Car",
        ],
        "Vehicle Size": ["Medsize", "Small", "Large"],
    }
    return claims_dict


def get_expanded_cols(df_csv, claims_dict):
    claims_colnames = []
    for header in claims_dict:
        if isinstance(df_csv[header].iloc[0], (np.int, np.int64)) or isinstance(
            df_csv[header].iloc[0], (np.float, np.float64)
        ):
            claims_colnames.append(header)
        else:
            claims_colnames.extend([header + "_" + str for str in claims_dict[header]])
    return claims_colnames



class NNPredictWrapper:
    def __init__(self, NN):
        self.NN = NN

    def predict(self, x):
        return np.squeeze(self.NN.predict(x), axis=1)


def pkl_path(project, model):
    return "models/{}_{}.pkl".format(project, model)


def pickle_model(model, scaler, model_name, test_error, description, filename):
    model_obj = {}
    model_obj["model"] = model
    model_obj["scaler"] = scaler
    model_obj["modelName"] = model_name
    model_obj["modelDescription"] = description
    model_obj["test_error"] = test_error
    model_obj["createdTime"] = int(time.time())
    with open(filename, "wb") as file:
        pickle.dump(model_obj, file)
    print(f"Saved: {model_name}")
