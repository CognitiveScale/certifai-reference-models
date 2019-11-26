import random
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import sys
sys.path.append("./")
from common_utils.train_utils import prep_diabetes_dataset, pickle_model


def train(msg):
    random.seed(0)
    training_data_uri = msg.payload.get("$ref", "./data/diabetes.csv")
    save_model_as = msg.payload.get('model_name')   
    X_train, X_test, y_train, y_test = prep_diabetes_dataset(training_data_uri)
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # start model training
    logit = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train,y_train)
    logit.score(X_test,y_test)
    logit_acc = logit.score(X_test,y_test)

    model_binary = f'models/{save_model_as}.pkl'
    pickle_model(
        logit,
        scaler,
        "LR",
        logit_acc,
        "Logistic Regression Classifier",
        model_binary,
    )
    print(logit_acc)
    return (f'model: {model_binary}')

