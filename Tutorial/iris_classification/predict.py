import json
import numpy as np
from sklearn import svm
from sklearn import datasets
from cortex import Message
from warnings import simplefilter
from typing import Dict, List
simplefilter(action='ignore', category=FutureWarning)


model_name = "iris_classification"

model_ctx = {}


def _train_create_sample_model() -> svm.classes.SVC:
    """
    for demonstration purposes, create a sample svc test model trained on iris dataset.
    users can load their own model in memory in any way suitable
    Returns: support vector classifier (svc) trained model

    """
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)
    return clf


def _create_test_data() -> str:
    """
    function to create sample test data from iris sklearn dataset. randomly pick 10 sample data points
    Returns: str: test_dataset (test_instances_generated.json) : fileName of the json-encoded test data created

    """
    test_dataset = "test_instances_generated.json"
    X, y = datasets.load_iris(return_X_y=True)
    test_data = {
        "payload": {
            "instances": X[np.random.randint(0, 150, 10)].tolist()
        }
    }
    with open(test_dataset, 'w') as fp:
        json.dump(test_data, fp, indent=4)
    return test_dataset


def predict_iris_type(msg: Message) -> Dict:
    """
    this function is called when api is invoked. loads the model and data instances.
    calls model.predict internally and returns list of prediction wrapped in python-dict object
    model_ctx: Dict: (global) loads model once and holds in memory till web service is running
    Args:
        msg: cortex message object

    Returns: dict containing list of predictions in-order

    """
    instances = msg.payload.get("instances", [])
    if model_name not in model_ctx:
        model_ctx[model_name] = _train_create_sample_model()
    instances = np.array(instances, dtype=object)
    instances = instances if instances.ndim == 2 else np.reshape(instances, (1, -1))
    model = model_ctx[model_name]
    predictions = model.predict(instances)
    return {"predictions": predictions.tolist()}


if __name__ == '__main__':
    """
    [optional] only when running file as python script
    [additional dependency] `pip install cortex-python==1.1.0` when running main
    """
    test_set = _create_test_data()
    with open(test_set) as fl:
        print(predict_iris_type(Message(json.load(fl))))
