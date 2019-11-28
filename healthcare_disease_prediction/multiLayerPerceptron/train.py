import random
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from healthcare_disease_prediction.common_utils.train_utils import prep_diabetes_dataset
from utils.encode_decode import pickle_model

def train(msg):
    random.seed(0)
    training_data_uri = msg.payload.get("$ref", "./data/diabetes.csv")
    save_model_as = msg.payload.get("model_name")
    X_train, X_test, y_train, y_test = prep_diabetes_dataset(training_data_uri)
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # start model training
    mlp = MLPClassifier(hidden_layer_sizes=(20, 20), max_iter=1000)
    mlp.fit(X_train, y_train)
    mlp.score(X_test, y_test)
    mlp_acc = mlp.score(X_test, y_test)
    model_binary = f"models/{save_model_as}.pkl"
    pickle_model(mlp, scaler, "MLP", mlp_acc, "Basic MLP model", model_binary)
    print(mlp_acc)
    return f"model: {model_binary}"

