import numpy as np

from example_utils import get_model


def predict(model_name, instances):
    instances = np.array(instances, dtype=object)
    instances = instances if instances.ndim == 2 else np.reshape(instances, (1, -1))

    model_use_case = model_name[:model_name.rfind('_')]
    model_variant = model_name[model_name.rfind('_')+1:]
    model_obj = get_model(model_use_case, model_variant)
    scaler = model_obj['scaler']
    if scaler:
        instances = scaler.transform(instances)

    predictions = model_obj['model'].predict(instances)
    return {'predictions': predictions.tolist()}
