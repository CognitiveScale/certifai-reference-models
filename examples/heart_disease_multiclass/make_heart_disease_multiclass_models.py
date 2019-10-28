from sklearn import preprocessing
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import warnings
import random
import pickle
import time
import os
from heart_disease_multiclass_encoder import CategoricalEncoder
from sklearn.metrics import accuracy_score

# supress all warnings
warnings.filterwarnings('ignore')

dirname = os.path.dirname(__file__)
def pkl_path(type):
    return os.path.join(dirname, 'models/heart_disease_multiclass_{}.pkl'.format(type))


if __name__ == "__main__":
    random.seed(2)
    np.random.seed(2)

    data = pd.read_csv(os.path.join(dirname, 'data/heart_disease_multiclass-prepped.csv'))
    feature_names = list(data.columns[:-1])

    # Separate outcome
    y = data['class_att']
    X = data.drop('class_att', axis=1)


    # apply encoder data
    scaler = CategoricalEncoder()
    scaler.fit(X)

    X_onehot = scaler.transform(X)

    #split test and training
    X_train, X_test, y_train, y_test = train_test_split(X_onehot, y, test_size=0.10, random_state = 0)

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


    from sklearn.linear_model import LogisticRegression
    logit = LogisticRegression(random_state=0, solver='lbfgs')
    logit.fit(X_train.values, y_train.values)
    logit_acc = logit.score(X_test.values, y_test.values)
    pickle_model(logit, scaler, 'LR', logit_acc, 'Logistic Regression Classifier', pkl_path('lr'))
    print(logit_acc)

    # Model 2:
    import xgboost as xgb
    from sklearn import metrics
    xgbt = xgb.XGBClassifier(objective="multi:softmax")
    xgbt.fit(X_train, y_train)
    preds = xgbt.predict_proba(X_test)
    y_pred = np.asarray([np.argmax(line) for line in preds])
    # evaluate predictions
    xgbt_acc =  metrics.accuracy_score(y_test, y_pred)
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
        'Model': ['aheart_disease_multiclass_logit', 'heart_disease_multiclass_xgb', 'heart_disease_multiclass_knn', 'heart_disease_multiclass_rf'],
        'Accuracy': [logit_acc, xgbt_acc, knn_acc, rf_acc]
    }
    METRICS_FILE = 'models/performance_metrics.csv'
    df = pd.DataFrame(data=metrics)
    df.to_csv(METRICS_FILE, index=False)
    print(f'Metrics written to {METRICS_FILE}\n')
