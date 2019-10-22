import time
import random
import pickle
import warnings
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from german_encoder import CategoricalEncoder

# supress all warnings
warnings.filterwarnings('ignore')

def main():
    random.seed(0)
    np.random.seed(0)

    data = pd.read_csv('data/german_credit-decoded.csv')
    feature_names = list(data.columns[:-1])

    # Separate outcome
    y = data['outcome']
    X = data.drop('outcome',axis=1)

    # apply encoder data
    scaler = CategoricalEncoder()
    scaler.fit(X)

    X_onehot = scaler.transform(X)
    X_onehot.head()

    # split test and training
    X_train, X_test, y_train, y_test = train_test_split(X_onehot, y, random_state = 0)

    #possible models
    from sklearn.tree import DecisionTreeClassifier
    dtree = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
    dtree.fit(X_train.values, y_train.values)
    dtree_acc = dtree.score(X_test.values,y_test.values)

    #other model
    from sklearn.neural_network import MLPClassifier
    mlp = MLPClassifier(hidden_layer_sizes=(20,20),max_iter=2000)
    mlp.fit(X_train.values, y_train.values)
    mlp_acc = mlp.score(X_test.values,y_test.values)

    # svm
    from sklearn import svm
    SVM = svm.SVC(gamma='scale')
    SVM.fit(X_train.values, y_train.values)
    svm_acc = SVM.score(X_test.values,y_test.values)

    # logistic
    from sklearn.linear_model import LogisticRegression
    logit = LogisticRegression(random_state=0, solver='lbfgs')
    logit.fit(X_train.values, y_train.values)
    logit_acc = logit.score(X_test.values,y_test.values)


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


    # Save models as pickle files
    pickle_model(dtree, scaler, 'Decision Tree', dtree_acc, 'Basic Decision Tree model', 'models/german_credit_dtree.pkl')
    pickle_model(logit, scaler, 'LOGIT', logit_acc, 'Basic LOGIT model', 'models/german_credit_logit.pkl')
    pickle_model(mlp, scaler, 'MLP', mlp_acc, 'Basic MLP model', 'models/german_credit_mlp.pkl')
    pickle_model(SVM, scaler, 'SVM', svm_acc, 'Basic SVM model', 'models/german_credit_svm.pkl')


    # write performance metrics to a file
    metrics = {
        'Model': ['german_credit_dtree', 'german_credit_logit', 'german_credit_mlp', 'german_credit_svm'],
        'Accuracy': [dtree_acc, logit_acc, mlp_acc, svm_acc]
    }
    METRICS_FILE = 'models/performance_metrics.csv'
    df = pd.DataFrame(data=metrics)
    df.to_csv(METRICS_FILE, index=False)
    print(f'Metrics written to {METRICS_FILE}\n')


if __name__ == "__main__":
    main()
