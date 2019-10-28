from sklearn import preprocessing
import pandas as pd
import numpy as np
import os
dirname = os.path.dirname(__file__)

def load_heart_disease_dict(df):
    df_dict = {}
    num_col_ = []
    cat_col_ = []
    for i in range(df.shape[1]):
        if df.iloc[:, i].dtype == 'object':
            df_dict[i] = df.iloc[:, i].unique().tolist()
            cat_col_ += [i]
        else:
            df_dict[i] = [df.columns[i]]
            num_col_ += [i]
    return df_dict, num_col_, cat_col_

data = pd.read_csv(os.path.join(dirname, 'data/heart_disease_multiclass-prepped.csv')) 
# Separate outcome
y = data['class_att']
X = data.drop('class_att', axis=1)


heart_disease_dict, num_col, cat_col = load_heart_disease_dict(X)


class CategoricalEncoder:
    def __init__(self):
        self.mean__ = 0
        self.scale_ = 1

    def encodeColumn(self, oldCol, labels):
        encoder = preprocessing.OneHotEncoder()
        encoder.fit(np.array(labels).reshape(-1, 1))

        to_transform = [[c] for c in oldCol]
        newCol = encoder.transform(to_transform)

        return newCol.toarray()

    def fit(self, X):
        # Compute the mean and std to be used for later scaling.

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
        all_column_names = [name for i in range(len(heart_disease_dict)) for name in heart_disease_dict[i]]
        trans_df = np.zeros((num_rows, len(all_column_names)))
        cur_col = 0
        feature_names = []

        for idx, header in enumerate(X):

            if idx in cat_col:
                encoded_col = self.encodeColumn(X[header], heart_disease_dict[idx])
                encoded_col = encoded_col.reshape((X.shape[0], len(heart_disease_dict[idx])))
            if idx in num_col:
                encoded_col = (X[header].values.astype(float) - self.mean_[idx]) / self.scale_[idx]
            
            # sorted due to OneHotEncoder returning a sorted encoding
            feature_names.extend(sorted(heart_disease_dict[idx]))
            encoded_col = encoded_col.reshape((num_rows, -1))

            end_col = cur_col + np.size(encoded_col, 1)
            trans_df[:, cur_col:end_col] = encoded_col
            cur_col = end_col

        # retain original ordering of input data encoding
        trans_df = pd.DataFrame(trans_df, columns=feature_names)
        a = list(trans_df.columns)
        return trans_df.reindex(columns=all_column_names)