import os
import time
import random
import pickle
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# supress all warnings
warnings.filterwarnings('ignore')

MODEL_FOLDER = 'models'

def prep_diabetes_dataset(): # we assume a pre-cleaned dataset
    dataset_path =f"data/diabetes.csv"
    with open(dataset_path, 'rb') as fl:
        data = pd.read_csv(dataset_path)
    data = data[(data.BloodPressure != 0) & (data.BMI != 0) & (data.Glucose != 0)]
    y = data['Outcome']
    X = data.drop('Outcome',axis=1)
    return train_test_split(X, y, random_state = 0)

def construct_model_obj(model, scaler, model_name, description):
    model_obj = {}
    model_obj['model'] = model
    model_obj['scaler'] = scaler
    model_obj['modelName'] = model_name
    model_obj['modelDescription'] = description
    model_obj['createdTime'] = int(time.time())
    return model_obj

def pickle_model(model_obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(model_obj, file)

def do_logit(X_train, X_test, y_train, y_test):
    from sklearn.linear_model import LogisticRegression
    logit = LogisticRegression(random_state=0, solver='lbfgs').fit(X_train,y_train)
    logit.score(X_test,y_test)
    logit_acc = logit.score(X_test,y_test)
    return logit, logit_acc

def do_svm(X_train, X_test, y_train, y_test):
    from sklearn import svm
    SVM = svm.SVC(gamma='scale')
    SVM.fit(X_train, y_train)
    SVM.score(X_test, y_test)
    svm_acc = SVM.score(X_test, y_test)
    return SVM, svm_acc

def do_mlp(X_train, X_test, y_train, y_test):
    from sklearn.neural_network import MLPClassifier
    mlp = MLPClassifier(hidden_layer_sizes=(20,20),max_iter=1000)
    mlp.fit(X_train, y_train)
    mlp.score(X_test, y_test)
    mlp_acc = mlp.score(X_test, y_test)
    return mlp, mlp_acc

def do_dtree(X_train, X_test, y_train, y_test):
    from sklearn.tree import DecisionTreeClassifier
    dtree = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
    dtree.fit(X_train, y_train)
    dtree_acc = dtree.score(X_test,y_test)
    return dtree, dtree_acc


train_functions = {
    'logit': do_logit,
    'svm': do_svm,
    'mlp': do_mlp,
    'dtree': do_dtree
}

def main():
    random.seed(0)
    np.random.seed(0)

    X_train, X_test, y_train, y_test = prep_diabetes_dataset()
    scaler = StandardScaler(copy=True, with_mean=True, with_std=True)
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    metrics = { 'Model': [], 'Accuracy': [] }
    for model_type, train_fn in train_functions.items():
        model_name = f"diabetes_{model_type}"
        model, acc = train_fn(X_train, X_test, y_train, y_test)
        model_path = os.path.join(MODEL_FOLDER, f"{model_name}.pkl")
        model_obj = construct_model_obj(model, scaler, model_name, f"diabetes model of type {model_type}")
        pickle_model(model_obj, model_path)
        print(f"Saved: {model_name}")
        metrics['Model'].append(model_name)
        metrics['Accuracy'].append(acc)

    # write performance metrics to a file
    METRICS_FILE = 'models/performance_metrics.csv'
    df = pd.DataFrame(data=metrics)
    df.to_csv(METRICS_FILE, index=False)
    print(f'Metrics written to {METRICS_FILE}\n')

if __name__ == '__main__':
    main()
