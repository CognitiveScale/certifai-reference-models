""" 
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""
from sklearn.preprocessing import StandardScaler

def prep_diabetes_dataset(data):  # we assume a pre-cleaned dataset
    return data[(data.BloodPressure != 0) & (data.BMI != 0) & (data.Glucose != 0)]


class WrappedStandardScaler(StandardScaler):
    # all of the data is numeric in this example and needs to be treated as float to avoid warnings
    def fit(self, d, **kwargs):
        return super().fit(d.astype(float), **kwargs)

    def transform(self, d, **kwargs):
        # all of the data is numeric and needs to be treated as float
        return super().transform(d.astype(float), **kwargs)
