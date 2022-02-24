""" 
Copyright (c) 2020. Cognitive Scale Inc. All rights reserved.
Licensed under CognitiveScale Example Code License https://github.com/CognitiveScale/certifai-reference-models/blob/450bbe33bcf2f9ffb7402a561227963be44cc645/LICENSE.md
"""
import numpy as np
import os
import pickle
import sys
from certifaiReferenceModelServer.utils.encode_decode import init_model
from certifaiReferenceModelServer.utils.local_server import assemble_server

model_name = os.getenv("MODElNAME", "customer_churn_mlp")

model_ctx = {}


# entrypoint for predict daemon
def predict_customer_churn_mlp(msg):
    instances = msg.get('payload', {}).get("instances", [])
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

if __name__ == '__main__':
    assemble_server(sys.argv[1])