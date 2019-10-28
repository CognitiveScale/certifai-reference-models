import config as cfg
from predict import predict
from example_utils import set_root

set_root(cfg.server['EXAMPLES_FOLDER'])

## TODO(la): create a singular s2i handler (or auto-generate these)?

# Auto insurance s2i handlers

def predict_auto_insurance_linl1(message):
    instances = message.payload.get('instances', [])
    return predict('auto_insurance_linl1', instances)

def predict_auto_insurance_linl2(message):
    instances = message.payload.get('instances', [])
    return predict('auto_insurance_linl2', instances)

def predict_auto_insurance_nn(message):
    instances = message.payload.get('instances', [])
    return predict('auto_insurance_nn', instances)

def predict_auto_insurance_rf(message):
    instances = message.payload.get('instances', [])
    return predict('auto_insurance_rf', instances)

def predict_auto_insurance_svr(message):
    instances = message.payload.get('instances', [])
    return predict('auto_insurance_svr', instances)


### diabetes s2i handlers

def predict_diabetes_svm(message):
    instances = message.payload.get('instances', [])
    return predict('diabetes_svm', instances)

def predict_diabetes_logit(message):
    instances = message.payload.get('instances', [])
    return predict('diabetes_logit', instances)

def predict_diabetes_mlp(message):
    instances = message.payload.get('instances', [])
    return predict('diabetes_mlp', instances)

def predict_diabetes_dtree(message):
    instances = message.payload.get('instances', [])
    return predict('diabetes_dtree', instances)


### german_credit s2i handlers

def predict_german_credit_svm(message):
    instances = message.payload.get('instances', [])
    return predict('german_credit_svm', instances)

def predict_german_credit_logit(message):
    instances = message.payload.get('instances', [])
    return predict('german_credit_logit', instances)

def predict_german_credit_mlp(message):
    instances = message.payload.get('instances', [])
    return predict('german_credit_mlp', instances)

def predict_german_credit_dtree(message):
    instances = message.payload.get('instances', [])
    return predict('german_credit_dtree', instances)


### customer_churn s2i handlers

def predict_customer_churn_mlp(message):
    instances = message.payload.get("instances", [])
    return predict("customer_churn_mlp", instances)

def predict_customer_churn_gbm(message):
    instances = message.payload.get("instances", [])
    return predict("customer_churn_gbm", instances)

def predict_customer_churn_svm(message):
    instances = message.payload.get("instances", [])
    return predict("customer_churn_svm", instances)

def predict_customer_churn_rf(message):
    instances = message.payload.get("instances", [])
    return predict("customer_churn_rf", instances)


### bank_marketing s2i handlers

def predict_bank_marketing_svm(message):
    instances = message.payload.get('instances', [])
    return predict('bank_marketing_svm', instances)

def predict_bank_marketing_logit(message):
    instances = message.payload.get('instances', [])
    return predict('bank_marketing_logit', instances)

def predict_bank_marketing_mlp(message):
    instances = message.payload.get('instances', [])
    return predict('bank_marketing_mlp', instances)

def predict_bank_marketing_dtree(message):
    instances = message.payload.get('instances', [])
    return predict('bank_marketing_dtree', instances)


### telco_customer_churn s2i handlers

def predict_telco_customer_churn_svm(message):
    instances = message.payload.get('instances', [])
    return predict('telco_customer_churn_svm', instances)

def predict_telco_customer_churn_dtree(message):
    instances = message.payload.get('instances', [])
    return predict('telco_customer_churn_dtree', instances)

def predict_telco_customer_churn_gbt(message):
    instances = message.payload.get('instances', [])
    return predict('telco_customer_churn_gbt', instances)

def predict_telco_customer_churn_logit(message):
    instances = message.payload.get('instances', [])
    return predict('telco_customer_churn_logit', instances)

def predict_telco_customer_churn_mlp(message):
    instances = message.payload.get('instances', [])
    return predict('telco_customer_churn_mlp', instances)
