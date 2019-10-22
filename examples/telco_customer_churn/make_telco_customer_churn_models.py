from sklearn import preprocessing
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import warnings
import random
import pickle
import time
import os
from telco_customer_churn_encoder import CategoricalEncoder

# supress all warnings
warnings.filterwarnings('ignore')

dirname = os.path.dirname(__file__)
def pkl_path(type):
    return os.path.join(dirname, 'models/telco_customer_churn_{}.pkl'.format(type))

if __name__ == "__main__":
    random.seed(0)
    np.random.seed(0)

    data = pd.read_csv(os.path.join(dirname, 'data/Telco_Customer_Churn-prepped.csv'))
    feature_names = list(data.columns[:-1])

    # Separate outcome
    y = data['Churn']
    X = data.drop('Churn', axis=1)


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
    from sklearn.tree import DecisionTreeClassifier
    dtree = DecisionTreeClassifier(criterion='entropy', random_state=0)
    dtree.fit(X_train.values, y_train.values)
    dtree_acc = dtree.score(X_test.values, y_test.values)
    pickle_model(dtree, scaler, 'DT', dtree_acc, 'Basic DecisionTree classifier model', pkl_path('dtree'))

    # Model 2:
    from sklearn.linear_model import LogisticRegression
    logit = LogisticRegression(random_state=0, solver='lbfgs')
    logit.fit(X_train.values, y_train.values)
    logit_acc = logit.score(X_test.values, y_test.values)
    pickle_model(logit, scaler, 'LR', logit_acc, 'Basic Logistic Regression  model', pkl_path('logit'))

    # Model 3: MLP
    from sklearn.neural_network import MLPClassifier
    mlp = MLPClassifier()
    mlp.fit(X_train, y_train)
    mlp_acc = mlp.score(X_test, y_test)
    pickle_model(mlp, scaler, 'MLP', mlp_acc, 'Basic MLP classifier model', pkl_path('mlp'))

    # Model 4: SVM
    from sklearn import svm
    SVM = svm.SVC(gamma='scale')
    SVM.fit(X_train.values, y_train.values)
    svm_acc = SVM.score(X_test.values, y_test.values)
    pickle_model(SVM, scaler, 'SVM', svm_acc, 'Basic SVM classifier model', pkl_path('svm'))

    # Model 5: GBT
    from sklearn.ensemble import GradientBoostingClassifier
    gb = GradientBoostingClassifier()
    gb.fit(X_train, y_train)
    gb_acc = gb.score(X_test, y_test)
    pickle_model(gb, scaler, 'GBCT', gb_acc, 'Basic gradient boosting classifier', pkl_path('gbt'))

    # write performance metrics to a file
    metrics = {
        'Model': ['telco_customer_churn_dtree', 'telco_customer_churn_logit', 'telco_customer_churn_mlp', 'telco_customer_churn_svm', 'telco_customer_churn_gbt'],
        'Accuracy': [dtree_acc, logit_acc, mlp_acc, svm_acc, gb_acc]
    }
    METRICS_FILE = 'models/performance_metrics.csv'
    df = pd.DataFrame(data=metrics)
    df.to_csv(METRICS_FILE, index=False)
    print(f'Metrics written to {METRICS_FILE}\n')

