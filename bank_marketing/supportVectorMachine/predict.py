import numpy as np
import os
import pickle
import sys
sys.path.append("./")
from common_utils.predict_utils import init_model

model_name = os.getenv("MODElNAME", "bank_marketing_svm")

model_ctx = {}


# entrypoint for predict daemon
def predict_bank_marketing_svm(msg):
    instances = msg.payload.get("instances", [])
    if not model_name in model_ctx:
        model_ctx[model_name] = init_model(model_name)
    return predict(model_ctx, instances)


# predict code goes here
def predict(model_ctx, instances):
    instances = np.array(instances, dtype=object)
    instances = instances if instances.ndim == 2 else np.reshape(instances, (1, -1))
    model_obj = model_ctx[model_name]
    scaler = model_obj["scaler"]
    if scaler:
        instances = scaler.transform(instances)

    predictions = model_obj["model"].predict(instances)
    return {"predictions": predictions.tolist()}

