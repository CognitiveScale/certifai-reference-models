import random
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from customer_churn_encoder import CategoricalEncoder

# import model builders
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.neural_network import MLPClassifier
import time
import pickle

# Scoring function
from sklearn.metrics import roc_auc_score, roc_curve
import warnings

warnings.filterwarnings("ignore")

def main():
    random.seed(0)
    np.random.seed(0)

    data = pd.read_csv("data/customer_churn-prepped.csv")
    feature_names = list(data.columns[:-1])

    # separate outcome
    y = data["Exited"]
    X = data.drop("Exited", axis=1)

    # apply category encoder
    scaler = CategoricalEncoder()
    scaler.fit(X)

    X_onehot = scaler.transform(X)

    # split test and training
    X_train, X_test, y_train, y_test = train_test_split(X_onehot, y, random_state = 0)

    # POSSIBLE MODELS

    # Random Forest

    rfMod = RandomForestClassifier(n_estimators=10, criterion="gini")
    rfMod.fit(X_train, y_train)
    # Compute the model accuracy on the given test data and labels
    rf_acc = rfMod.score(X_test, y_test)
    # Return probability estimates for the test data
    test_labels = rfMod.predict_proba(np.array(X_test.values))[:, 1]
    # Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC) from prediction scores
    rf_roc_auc = roc_auc_score(y_test, test_labels, average="macro")

    # Support Vector Machine
    from sklearn import svm
    svmMod = svm.SVC(gamma='scale')
    svmMod.fit(X_train.values, y_train.values)
    svm_acc = svmMod.score(X_test.values, y_test.values)

    # GradientBoosting

    gbMod = GradientBoostingClassifier(loss="deviance", n_estimators=200)
    gbMod.fit(X_train, y_train)
    # Compute the model accuracy on the given test data and labels
    gb_acc = gbMod.score(X_test, y_test)
    # Return probability estimates for the test data
    test_labels = gbMod.predict_proba(np.array(X_test.values))[:, 1]
    # Compute Area Under the Receiver Operating Characteristic Curve (ROC AUC) from prediction scores
    gb_roc_auc = roc_auc_score(y_test, test_labels, average="macro")

    # MultiLayerPerceptron

    mlpMod = MLPClassifier()
    mlpMod.fit(X_train, y_train)
    mlpMod.score(X_test, y_test)
    mlp_acc = mlpMod.score(X_test, y_test)

    def pickle_model(model, scaler, model_name, test_accuracy, description, filename):
        model_obj = {}
        model_obj["model"] = model
        model_obj["scaler"] = scaler
        model_obj["modelName"] = model_name
        model_obj["modelDescription"] = description
        model_obj["test_acc"] = test_accuracy
        model_obj["createdTime"] = int(time.time())
        with open(filename, "wb") as file:
            pickle.dump(model_obj, file)
        print(f"Saved: {model_name}")

    # Save models as pickle files
    pickle_model(
        mlpMod,
        scaler,
        "MLP",
        mlp_acc,
        "Basic MLP classifier model",
        "models/customer_churn_mlp.pkl",
    )
    pickle_model(
        gbMod,
        scaler,
        "GBM",
        gb_acc,
        "Gradient Boosting Model",
        "models/customer_churn_gbm.pkl",
    )
    pickle_model(
        svmMod,
        scaler,
        "SVM",
        svm_acc,
        "Support Vector Machines",
        "models/customer_churn_svm.pkl",
    )
    pickle_model(
        rfMod,
        scaler,
        "RF",
        rf_acc,
        "Basic Random Forest Model",
        "models/customer_churn_rf.pkl",
    )

    # write performance metrics to a file
    metrics = {
        'Model': ['customer_churn_mlp', 'customer_churn_gbm', 'customer_churn_svm', 'customer_churn_rf'],
        'Accuracy': [mlp_acc, gb_acc, svm_acc, rf_acc]
    }
    METRICS_FILE = 'models/performance_metrics.csv'
    df = pd.DataFrame(data=metrics)
    df.to_csv(METRICS_FILE, index=False)
    print(f'Metrics written to {METRICS_FILE}\n')

if __name__ == "__main__":
    main()
