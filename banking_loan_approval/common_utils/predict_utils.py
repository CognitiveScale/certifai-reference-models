import pickle

def init_model(model_name):
    print(f"loading {model_name} ")
    fl = f"models/{model_name}.pkl"
    with open(fl, "rb") as f:
        return pickle.load(f)