from sklearn import preprocessing
import pandas as pd
import numpy as np
import os


# Hacky way to get correct data path when training and invoking model
cwd = os.path.basename(os.getcwd())
DATA_FILE = 'data/bank_marketing-prepped.csv'
DATA_FILE = 'examples/bank_marketing/' + DATA_FILE if cwd != 'bank_marketing' else DATA_FILE


def load_bank_marketing_dict(df):
    df_dict = {}
    num_col = []
    cat_col = []
    for i in range(df.shape[1]):

        if df.iloc[:, i].dtype == 'object':
            df_dict[i] = df.iloc[:, i].unique().tolist()
            cat_col += [i]
        else:
            df_dict[i] = [df.columns[i]]
            num_col += [i]
    return df_dict, num_col, cat_col


data = pd.read_csv(DATA_FILE)

X = data.drop(['deposit'], axis=1)
y = data['deposit']


bank_dict, num_col, cat_col = load_bank_marketing_dict(X)


class CategoricalEncoder():
    def __init__(self):
        self.mean__ = 0
        self.scale_ = 1

    def encodeColumn(self, oldCol, labels):
        encoder = preprocessing.OneHotEncoder()
        encoder.fit(np.array(labels).reshape(-1,1))

        to_transform = [[c] for c in oldCol]
        newCol = encoder.transform(to_transform)

        return newCol.toarray()

    def fit(self, X):
        #Compute the mean and std to be used for later scaling.

        self.mean_ = np.zeros(X.shape[1])
        self.scale_ = np.ones(X.shape[1])

        X_numeric = X.iloc[:, num_col]

        scaler = preprocessing.StandardScaler().fit((X_numeric.values).astype(float))

        self.mean_[num_col] = scaler.mean_
        self.scale_[num_col] = scaler.scale_

        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        num_rows = X.shape[0]
        all_column_names = [name for i in range(len(bank_dict)) for name in bank_dict[i]]
        trans_df = np.zeros((num_rows, len(all_column_names)))
        cur_col = 0
        feature_names = []

        for idx, header in enumerate(X):

            if idx in cat_col:
                encoded_col = self.encodeColumn(X[header], bank_dict[idx])
                encoded_col = encoded_col.reshape((X.shape[0], len(bank_dict[idx])))
            if idx in num_col:
                encoded_col = ((X[header].values).astype(float) - self.mean_[idx])/self.scale_[idx]

            # sorted due to OneHotEncoder returning a sorted encoding
            feature_names.extend(sorted(bank_dict[idx]))
            encoded_col = encoded_col.reshape((num_rows, -1))

            end_col = cur_col + np.size(encoded_col, 1)
            trans_df[:, cur_col:end_col] = encoded_col
            cur_col = end_col

        # retain original ordering of input data encoding
        trans_df = pd.DataFrame(trans_df, columns=feature_names)
        return trans_df.reindex(columns=all_column_names)
