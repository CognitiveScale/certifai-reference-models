import os
import time
import pickle
import random
import warnings
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from auto_insurance_encoder import CategoricalEncoder, NNPredictWrapper

# supress all warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)



def main():
    random.seed(0)
    np.random.seed(0)

    data = pd.read_csv('data/auto_insurance_claims_dataset.csv')

    # Getting feature names
    feature_names = list(data.columns)
    feature_names.remove('Total Claim Amount')

    # Train-test split
    X = data.copy()
    y = X['Total Claim Amount']
    X_tr, X_tst, y_tr, y_tst = train_test_split(X,y,test_size=1000, random_state = 0)

    # Tranforming train and test data
    scaler = CategoricalEncoder()
    scaler.fit(X_tr)
    X_train = scaler.transform(X_tr.drop(['Total Claim Amount'],axis=1))
    y_train = X_tr['Total Claim Amount']

    X_test = scaler.transform(X_tst.drop(['Total Claim Amount'],axis=1))
    y_test = X_tst['Total Claim Amount']


    # Linear model, L1 regularization, Lasso Model
    from sklearn.linear_model import Lasso
    lmodel_l1 = Lasso(alpha=1e-4, copy_X=True, fit_intercept=True, max_iter=1000,
         normalize=False, positive=False, precompute=False, random_state=None,
         selection='cyclic', tol=0.0001, warm_start=False)
    lmodel_l1.fit(X_train,y_train)
    y_pred = lmodel_l1.predict(X_test)
    l1_err = ((y_test-y_pred)**2).sum() # Prediction error

    # Linear model, L2 regularization, Lasso Model
    from sklearn.linear_model import Ridge
    lmodel_l2 = Ridge(alpha=0.1, copy_X=True, fit_intercept=True, max_iter=1000,
         normalize=False, random_state=None, tol=0.0001)
    lmodel_l2.fit(X_train,y_train)
    y_pred = lmodel_l2.predict(X_test)
    l2_err = ((y_test-y_pred)**2).sum() # Prediction error

    # Neural Network model
    from keras.models import Sequential
    from keras.layers import Dense
    NN = Sequential()
    NN.add(Dense(1000, input_dim=X_train.shape[1],  activation='relu'))
    NN.add(Dense(200, activation='relu'))
    NN.add(Dense(50, activation='relu'))
    NN.add(Dense(1))
    NN.summary()

    NN.compile(loss='mse', optimizer='adam', metrics=['mse','mae'])
    NN.fit(X_train, y_train, epochs=500, batch_size=300,  verbose=0)

    # Random Forest model
    from sklearn.ensemble import RandomForestRegressor
    rf = RandomForestRegressor(n_estimators = 10, max_depth=11,bootstrap=True)
    rf.fit(X_train,y_train)
    y_pred = rf.predict(X_test)
    rf_err = ((y_test-y_pred)**2).sum() # Prediction error

    # Support Vector Regression
    from sklearn.svm import SVR
    svr = SVR(kernel = 'rbf', C=50.0)
    svr.fit(X_train,y_train)
    y_pred = svr.predict(X_test)
    svr_err = ((y_test-y_pred)**2).sum() # Prediction error

    # function to pickle our models for later access
    def pickle_model(model, scaler, model_name, description, filename):
        model_obj = {}
        model_obj['model'] = model
        model_obj['scaler'] = scaler
        model_obj['modelName'] = model_name
        model_obj['modelDescription'] = description
        model_obj['createdTime'] = int(time.time())
        with open(filename, 'wb') as file:
            pickle.dump(model_obj, file)
        print(f"Saved: {model_name}")

    # save models as pickle files
    pickle_model(lmodel_l1,scaler,'Linear L1','Linear regression with L1 regularization','models/auto_insurance_linl1.pkl')
    pickle_model(lmodel_l2,scaler,'Linear L2','Linear regression with L2 regularization', 'models/auto_insurance_linl2.pkl')
    pickle_model(NNPredictWrapper(NN),scaler,'Neural Network','Four-layer neural network', 'models/auto_insurance_nn.pkl')
    pickle_model(rf,scaler,'Random Forest','Random forest', 'models/auto_insurance_rf.pkl')
    pickle_model(svr,scaler,'SVR','Support vector regression', 'models/auto_insurance_svr.pkl')


    # Computing R0-squared of trained models on test set
    from sklearn.metrics import r2_score

    mse_scores = []
    model_files = ['models/auto_insurance_linl1.pkl','models/auto_insurance_linl2.pkl','models/auto_insurance_nn.pkl',
                   'models/auto_insurance_rf.pkl','models/auto_insurance_svr.pkl']
    for f in model_files:
        with open(f, 'rb') as fl:
            model_obj = pickle.load(fl)
        y_pred = model_obj['model'].predict(X_test) # Preidction using model on test set
        err = r2_score(y_test,y_pred)
        mse_scores.append(err)

    # write performance metrics to a file
    metrics = {
        'Model': ['auto_insurance_linl1', 'auto_insurance_linl2', 'auto_insurance_nn', 'auto_insurance_rf', 'auto_insurance_svr'],
        'R-squared': mse_scores
    }
    METRICS_FILE = 'models/performance_metrics.csv'
    df = pd.DataFrame(data=metrics)
    df.to_csv(METRICS_FILE, index=False)
    print(f'Metrics written to {METRICS_FILE}\n')



if __name__ == '__main__':
    main()
