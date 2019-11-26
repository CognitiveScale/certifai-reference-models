import numpy as np
import os
import pickle
import sys
sys.path.append("./")
from common_utils.predict_utils import init_model


from logisticRegression.predict import predict_german_credit_logit
from decisionTree.predict import predict_german_credit_dtree
from multiLayerPerceptron.predict import predict_german_credit_mlp
from supportVectorMachine.predict import predict_german_credit_svm

