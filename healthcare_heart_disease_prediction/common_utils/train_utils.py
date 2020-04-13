from sklearn import preprocessing
import pandas as pd
import numpy as np


class CategoricalEncoder:
    def __init__(self, df):
        self.df = df
        self.mean__ = 0
        self.scale_ = 1
        self.data_dict__ = {}
        self.num_col__ = []
        self.cat_col__ = []
        self.infer_from_dataset()

    def encodeColumn(self, oldCol, labels):
        encoder = preprocessing.OneHotEncoder()
        encoder.fit(np.array(labels).reshape(-1, 1))

        to_transform = [[c] for c in oldCol]
        newCol = encoder.transform(to_transform)

        return newCol.toarray()

    def infer_from_dataset(self):
        df_dict = {}
        num_col = []
        cat_col = []
        for i in range(self.df.shape[1]):
          if self.df.iloc[:, i].dtype == 'object':
              df_dict[i] = self.df.iloc[:, i].unique().tolist()
              cat_col += [i]
          else:
              df_dict[i] = [self.df.columns[i]]
              num_col += [i]

        self.data_dict__ = df_dict
        self.num_col__ = num_col
        self.cat_col__ = cat_col

    def fit(self, X):
        # Compute the mean and std to be used for later scaling.

        self.mean_ = np.zeros(X.shape[1])
        self.scale_ = np.ones(X.shape[1])

        X_numeric = X.iloc[:, self.num_col__]

        scaler = preprocessing.StandardScaler().fit((X_numeric.values).astype(float))

        self.mean_[self.num_col__] = scaler.mean_
        self.scale_[self.num_col__] = scaler.scale_

        return self

    def transform(self, X):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        num_rows = X.shape[0]
        all_column_names = [name for i in range(
            len(self.data_dict__)) for name in self.data_dict__[i]]
        trans_df = np.zeros((num_rows, len(all_column_names)))
        cur_col = 0
        feature_names = []

        for idx, header in enumerate(X):

            if idx in self.cat_col__:
                encoded_col = self.encodeColumn(
                    X[header], self.data_dict__[idx])
                encoded_col = encoded_col.reshape(
                    (X.shape[0], len(self.data_dict__[idx])))
            if idx in self.num_col__:
                encoded_col = (X[header].values.astype(
                    float) - self.mean_[idx]) / self.scale_[idx]

            # sorted due to OneHotEncoder returning a sorted encoding
            feature_names.extend(sorted(self.data_dict__[idx]))
            encoded_col = encoded_col.reshape((num_rows, -1))

            end_col = cur_col + np.size(encoded_col, 1)
            trans_df[:, cur_col:end_col] = encoded_col
            cur_col = end_col

        # retain original ordering of input data encoding
        trans_df = pd.DataFrame(trans_df, columns=feature_names)
        a = list(trans_df.columns)
        return trans_df.reindex(columns=all_column_names)
