
<center> <h1>Cortex Certifai Sandbox Case-Studies </h1> </center>

Section below contains details of Certifai Evaluation components that are common across each evaluation [use case / project]

   > _[Glossary of common terms](#Glossary)_

###  <a id="Models">**Models**</a>

This tab includes:
 - List of ML Models that are to evaluated using Cortex Certifai

### <a id="Datasets"> **Evaluation Dataset**</a> 
   This tab includes:
 - an `Evaluation Dataset` of **X** no. of instances, used to assess global properties such as model robustness and fairness
 - **X** `Rows Explanations Dataset` containing **X** no. of <a id="Observations">instances</a> for which counterfactual (CF) explanations are desired

### <a id="Evaluations">**Evaluations**</a>
This tab shows the following evaluation results:
- `Robustness`: Robustness is compared across all the pre-built models. 
  > _Higher means more robust_
- `Fairness`: For Fairness, first the desired outcome along with the grouping feature needs to be specified. Panel on the left shows the fairness scores (_Higher is fairer_) for all the pre-built models. Panel on the Right compares the burden across the sub-groups specified by the grouping feature
   > _similar bar lengths indicate fairer models_
  
- `Explanations`: Here one can specify the model (e.g. SVM) and the [observation (#)](#Observations), and then the CF explanation is displayed by highlighting the fields that change. 

--- 

## Use Cases Around Binary Classification 


### <b>Banking: Loan Approval</b>

  - In this use case, each entry in the [dataset](#Datasets) represents a person who takes a credit loan from a bank
  - Learning task is to classify each person as either a good or bad credit risk based on the set of attributes of that person. 
  - Model predicts whether loan will be _granted_ or _not-granted_ based on the credit risk evaluation
  - This dataset was sourced from [Kaggle](https://www.kaggle.com/uciml/german-credit). Originally from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data))

  This use-case comes with 4 pre-trained [models](#Models), based respectively on 
  - SVM
  - Logistic Regression
  - Decision Tree
  - Multi-Layered Perceptron. 
  
  [Evaluations](#Evaluations):
   - Robustness
   - Fairness 
   - Explanations
---

### <b>HealthCare: Disease Prediction</b>

-  In this use case, each entry in the dataset represents a patient
-  Learning task is to predict whether or not a patient has diabetes, based on certain diagnostic measurements included in the dataset
- Several constraints were placed on the selection of these instances from a larger database
- In particular, all patients here are females at least 21 years old of Pima Indian heritage
- This dataset was sourced from [Kaggle](https://www.kaggle.com/uciml/pima-indians-diabetes-database ). Originally from the [National Institute of Diabetes and Digestive and Kidney Diseases](https://www.niddk.nih.gov/)

This use-case comes with 4 pre-trained models, based respectively on 
  - SVM
  - Logistic Regression
  - Decision Tree
  - Multi-Layered Perceptron. 

   [Evaluations](#Evaluations):
   - Robustness
   - Explanations 
---

### <b>Banking: Propensity to Buy</b>

-  In this use case, each entry in the dataset represents a target of a previous marketing campaign
-  Learning task is to predict who will make a term deposit with the bank as a result of a similar campaign
- This dataset was sourced from [Kaggle](https://www.kaggle.com/janiobachmann/bank-marketing-dataset). Originally from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Bank+Marketing)

This use-case comes with 4 pre-trained models, based respectively on 
  - SVM
  - Logistic Regression
  - Decision Tree
  - Multi-Layered Perceptron. 

   [Evaluations](#Evaluations):
   - Robustness
   - Fairness 
   - Explanations 
---

### <b>Banking: Predicting Customer Churn</b>

-  In this use case, each entry in the dataset represents a customer or previous customer of the bank
-  Learning task is to predict who is likely to quit as a customer
- This dataset was sourced from [Kaggle](https://www.kaggle.com/adammaus/predicting-churn-for-bank-customers)

This use-case comes with 4 pre-trained models, based respectively on 
  - SVM
  - Random Forest
  - Gradient Boosting
  - Multi-Layered Perceptron. 

   [Evaluations](#Evaluations):
   - Robustness
   - Fairness 
   - Explanations 
---

### <b>Finance: Income Prediction</b>

-  In this use case, each entry in the dataset represents attributes of a de-identified individual
-  Learning task is to predict the income bracket of the individual, which has two possible values `>50K` and `<=50K`
- This dataset was sourced from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/census+income)

This use-case comes with 3 pre-trained models, based respectively on 
  - Logistic Regression
  - Random Forest
  - XGBoost

   [Evaluations](#Evaluations):
   - Robustness
   - Fairness 
   - Explanations 
---

## Use Cases Around Predicting a Numeric Value (Regression/Function approximation) 


### <b>Insurance: Auto Insurance Claims</b>

-  In this use case, each entry in the dataset represents an auto insurance claim
-  Learning task is to predict the final settled claim amount
- This dataset was sourced from [Emcien](https://www.sixtusdakurah.com/resources/The_Application_of_Regularization_in_Modelling_Insurance_Claims.pdf)

This use-case comes with 5 pre-trained models, based respectively on 
  - L1 Linear Regression
  - L2 Linear Regression
  - Neural Network
  - Random Forest Regressor
  - SVR

   [Evaluations](#Evaluations):
   - Robustness
   - Fairness 
   - Explanations 
---


#### <a id="Glossary"></a><i>Commonly Referenced Terms ###

| Terms  | Meaning |
| ------ | ------ |
|   Models |  Machine Learning models that are to be evaluated using Certifai|
| Counterfactual | Alternative suggested datapoints that represent the amount of change required to move from one outcome to another  |
| Robustness |  Measure of how well models retain an outcome given changes to the data feature values<br>The more robust a model is the greater the changes required to alter the outcome |
| Fairness | Measure of difference required to change the outcome for different groups implicit in a feature given the same model and dataset
| Explanations | Predictive analysis provided through the generation of counterfactuals for the change that must occur in a dataset with given restrictions to obtain a different outcome  |



