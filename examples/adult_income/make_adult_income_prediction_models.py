from sklearn import preprocessing
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import warnings
import random
import pickle
import time
import os
from adult_income_prediction_encoder import CategoricalEncoder
from sklearn.metrics import accuracy_score

# supress all warnings
warnings.filterwarnings('ignore')

dirname = os.path.dirname(__file__)
def pkl_path(type):
    return os.path.join(dirname, 'models/adult_income_{}.pkl'.format(type))


if __name__ == "__main__":
    random.seed(0)
    np.random.seed(0)

    data = pd.read_csv(os.path.join(dirname, 'data/adult_income-prepped.csv'))
    feature_names = list(data.columns[:-1])

    # Separate outcome
    y = data['income']
    X = data.drop('income', axis=1)


    # apply encoder data
    scaler = CategoricalEncoder()
    scaler.fit(X)

    X_onehot = scaler.transform(X)

    #split test and training
    X_train, X_test, y_train, y_test = train_test_split(X_onehot, y, test_size=0.25, random_state=4)

    # function to pickle our models for later access
    def pickle_model(model, scaler, model_name, test_accuracy, description, filename):
        model_obj = {}
        model_obj['model'] = model
        model_obj['scaler'] = scaler
        model_obj['modelName'] = model_name
        model_obj['modelDescription'] = description
        model_obj['test_acc'] = test_accuracy
        model_obj['createdTime'] = int(time.time())
        with open(filename, 'wb') as file:
            pickle.dump(model_obj, file)
        print(f"Saved: {model_name}")

    # Model 1:
    from sklearn.linear_model import LogisticRegression
    logit = LogisticRegression(random_state=0, solver='lbfgs')
    logit.fit(X_train.values, y_train.values)
    logit_acc = logit.score(X_test.values, y_test.values)
    pickle_model(logit, scaler, 'LR', logit_acc, 'Logistic Regression Classifier', pkl_path('lr'))
    print(logit_acc)

    # Model 2:
    import xgboost as xgb
    xgbt = xgb.XGBClassifier(objective="binary:logistic", random_state=42)
    xgbt.fit(X_train, y_train)
    y_pred = xgbt.predict(X_test)
    predictions = [round(value) for value in y_pred]
    # evaluate predictions
    xgbt_acc = accuracy_score(y_test, predictions)
    pickle_model(xgbt, scaler, 'XGBoost', xgbt_acc, 'Extreme Gradient Boosting Classifier', pkl_path('xgb'))
    print(xgbt_acc)

    # Model 3:
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier()
    knn.fit(X_train, y_train)
    knn_acc = knn.score(X_test,y_test)
    pickle_model(knn, scaler, 'KNN', knn_acc, 'K Nearest Neighbor Classifier', pkl_path('knn'))
    print(knn_acc)

    # Model 4:
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier()
    rf.fit(X_train, y_train)
    rf_acc = rf.score(X_test,y_test)
    pickle_model(rf, scaler, 'RF', rf_acc, 'Random Forest Classifier', pkl_path('rf'))
    print(rf_acc)

     # write performance metrics to a file
    metrics = {
        'Model': ['adult_income_logit', 'adult_income_xgb', 'adult_income_knn', 'adult_income_rf'],
        'Accuracy': [logit_acc, xgbt_acc, knn_acc, rf_acc]
    }
    METRICS_FILE = 'models/performance_metrics.csv'
    df = pd.DataFrame(data=metrics)
    df.to_csv(METRICS_FILE, index=False)
    print(f'Metrics written to {METRICS_FILE}\n')