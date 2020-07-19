import time
import random
import pickle
import warnings
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from certifai.common.utils.encoding import CatEncoder


def main():
    random.seed(0)
    np.random.seed(0)

    data = pd.read_csv('data/german_credit.csv')

    # Separate outcome
    y = data['outcome']
    X = data.drop('outcome',axis=1)

    # apply encoder data
    cat_columns = [
        'checkingstatus',
        'history',
        'purpose',
        'savings',
        'employ',
        'status',
        'others',
        'property',
        'age',
        'otherplans',
        'housing',
        'job',
        'telephone',
        'foreign'
    ]

    encoder = CatEncoder(cat_columns, X, normalize=True)

    # split test and training
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 0)
    encoded_X_train = encoder(X_train.values)
    encoded_X_test = encoder(X_test.values)

    #possible models
    from sklearn.tree import DecisionTreeClassifier
    dtree = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
    dtree.fit(encoded_X_train, y_train.values)
    dtree_acc = dtree.score(encoded_X_test,y_test.values)

    #other model
    from sklearn.neural_network import MLPClassifier
    mlp = MLPClassifier(hidden_layer_sizes=(20,20),max_iter=2000)
    mlp.fit(encoded_X_train, y_train.values)
    mlp_acc = mlp.score(encoded_X_test,y_test.values)

    # svm
    from sklearn import svm
    SVM = svm.SVC(gamma='scale')
    SVM.fit(encoded_X_train, y_train.values)
    svm_acc = SVM.score(encoded_X_test,y_test.values)

    # logistic
    from sklearn.linear_model import LogisticRegression
    logit = LogisticRegression(random_state=0, solver='lbfgs')
    logit.fit(encoded_X_train, y_train.values)
    logit_acc = logit.score(encoded_X_test,y_test.values)

    # function to pickle our models for later access
    def pickle_model(model, encoder, model_name, test_accuracy, description, filename):
        model_obj = {'model': model, 'encoder': encoder, 'modelName': model_name,
                     'modelDescription': description, 'test_acc': test_accuracy,
                     'createdTime': int(time.time())}
        if not os.path.exists('models'):
            os.mkdir('models')
        with open(filename, 'wb') as file:
            pickle.dump(model_obj, file)
        print(f"Saved: {model_name}")

    # Save models as pickle files
    pickle_model(dtree, encoder, 'Decision Tree', dtree_acc, 'Basic Decision Tree model',
                 'models/german_credit_dtree.pkl')
    pickle_model(logit, encoder, 'LOGIT', logit_acc, 'Basic LOGIT model',
                 'models/german_credit_logit.pkl')
    pickle_model(mlp, encoder, 'MLP', mlp_acc, 'Basic MLP model',
                 'models/german_credit_mlp.pkl')
    pickle_model(SVM, encoder, 'SVM', svm_acc, 'Basic SVM model',
                 'models/german_credit_svm.pkl')


if __name__ == "__main__":
    main()
