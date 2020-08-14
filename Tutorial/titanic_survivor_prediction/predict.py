""" 
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing.data import StandardScaler
from cortex import Message
from typing import Dict, Tuple
from train import train_model
from sklearn.exceptions import DataConversionWarning
import warnings

warnings.filterwarnings(action='ignore', category=DataConversionWarning)

model_name = "titanic_survivor_prediction"
std_scaler = None
model_ctx = {}


def _train_sample_model() -> Tuple[RandomForestClassifier, StandardScaler]:
    """
    for demonstration purposes, create a sklearn.ensemble.RandomForestClassifier test model trained on titanic dataset(seaborn).
    users can load their own model in memory in any way suitable
    Returns: tuple of (rf_model:RandomForestClassifier,std_scaler:StandardScaler)

    """

    rf_model, std_scaler = train_model()
    return rf_model, std_scaler


def _create_api_test_data(encoded_dataset) -> Dict:
    """
    function to create 10 sample data instances to test predict api created from `encoded` titanic dataset(seaborn.load_dataset('titanic'))
    Args:
        encoded_dataset: encoded titanic dataset as csv
    Returns: Dict: test_api_instance:
    """

    test_api_instance = {
        "payload": {
            "instances": pd.read_csv(encoded_dataset).iloc[:10, 1:].values.tolist()
        }
    }
    with open('test_instances_generated.json', 'w') as fp:
        json.dump(test_api_instance, fp, indent=4)
    return test_api_instance


def predict_titanic_survivor(msg: Message) -> Dict:
    """
    this function is called when api is invoked. loads the model,scaler and data instances.
    calls sklearn `model.predict` internally and returns list of prediction wrapped in python-dict object
    model_ctx: Dict: (global) loads model once and holds in memory till web service is running
    Args:
        msg: cortex message object

    Returns: dict containing list of in-order predictions

    """
    global model_name, std_scaler
    instances = msg.payload.get("instances", [])
    if model_name not in model_ctx:
        model_ctx[model_name], std_scaler = _train_sample_model()
    instances = np.array(instances, dtype=object)
    instances = instances if instances.ndim == 2 else np.reshape(instances, (1, -1))
    predictions = model_ctx[model_name].predict(std_scaler.transform(instances))
    return {"predictions": predictions.tolist()}


if __name__ == '__main__':
    """
    [optional]:
        when running as python script
        'pip install -r requirements_local.txt` to install local dependencies
    """
    test_set = _create_api_test_data('encoded_dataset.csv')
    print(predict_titanic_survivor(Message(test_set)))
