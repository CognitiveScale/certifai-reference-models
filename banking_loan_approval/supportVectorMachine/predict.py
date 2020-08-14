import numpy as np
import os
import sys
from utils.encode_decode import init_model
from utils.local_server import assemble_server
model_name = os.getenv("MODElNAME", "german_credit_svm")

model_ctx = {}


# entrypoint for predict daemon
def predict_german_credit_svm(msg):
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
    scores = model_obj["model"].predict_proba(instances)
    labels = model_obj["model"].classes_
    return {
        "predictions": predictions.tolist(),
        "scores": scores.tolist(),
        "labels": labels.tolist()
    }

if __name__ == '__main__':
    assemble_server(sys.argv[1])