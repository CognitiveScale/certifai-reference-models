
# Banking: Loan Approval(German Credit)

## <b>Banking: Loan Approval</b>

**Learning Task Type**: Binary Classification

**Description**: Each dataset row represents the attribute values of a loan application. The models predict whether a loan will be granted or denied.

**Dataset Source**: [Kaggle](https://www.kaggle.com/uciml/german-credit) - Originally from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)

**Pre-trained Models**:

  - SVM
  - Logistic Regression
  - Decision Tree
  - Multi-layered Perception

**Evaluation Types**:

  - Robustness
  - Fairness
  - Explainability
  - Explanations


## Prerequisites  
1. [Source-to-Image](https://github.com/openshift/source-to-image)
2. Make
3. (Optional) [Httpie](https://httpie.org/) (only if you want to run ```make test-endpoint```)

## Quick Start
1. ### Model train (e.g. decisionTree)
	1. `cd decisionTree`
	2. build train-container `make build-train`
	3. run train-container `make train`
2.	### Model Predict
	1.	`cd decisionTree`
	2.	build predict-container `make build-predict`
	3.	run predict-container `make predict`

3. ### Run test:
	 1.	`cd decisionTree`
	 2.	`make test-endpoint`


## Build & Run all models together

1.	`cd all`
2.	to train all models `make train-all`
3.	to predict all models `make predict-all` 
