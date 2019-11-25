import numpy as np
import os
import pickle
import sys
sys.path.append("./")
from common_utils.predict_utils import init_model


from logisticRegression.predict import predict_adult_income_lr
from randomForest.predict import predict_adult_income_rf
from xgBoost.predict import predict_adult_income_xgb


