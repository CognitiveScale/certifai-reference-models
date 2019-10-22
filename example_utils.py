import os
import sys
import pickle
import pandas as pd


models = {}


def _find_example(model_use_case):
    example_dir = os.path.join(EXAMPLES_FOLDER, model_use_case)
    return example_dir


def set_root(directory):
    global EXAMPLES_FOLDER
    EXAMPLES_FOLDER = directory


def get_model(model_use_case, model_variant):
    model_name = f'{model_use_case}_{model_variant}'
    if model_name not in models or not models[model_name]:
        example_dir = _find_example(model_use_case)
        if example_dir not in sys.path:
            sys.path.append(example_dir) # update sys.path to fix example imports

        model_path = os.path.join(example_dir, 'models', f'{model_name}.pkl')
        with open(model_path, 'rb') as fl:
            models[model_name] = pickle.load(fl)
    return models[model_name]


def load_data(model_use_case, limit=-1):
    example_dir = _find_example(model_use_case)
    data_dir = os.path.join(example_dir, 'data')
    for f in os.listdir(data_dir):
        if f.endswith('.csv'):
            data = pd.read_csv(os.path.join(data_dir, f))
            if limit > 0:
                data = data[:limit]
            return data
    raise ValueError(f"Model data for model '{model_use_case}' not found")
