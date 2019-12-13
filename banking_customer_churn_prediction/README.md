# Banking: Predicting Customer Churn

**Learning Task Type**: Binary Classification

**Description**: Each dataset row represents the attribute values for the target of a previous marketing campaign. The models predict whether a similar campaign will result in the target making a deposit at the bank.

**Dataset Source**: [Kaggle](https://www.kaggle.com/adammaus/predicting-churn-for-bank-customers)

**Pre-trained Models**:

  - SVM
  - Random Forest
  - Gradient Boosting
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
1. ### Model train (e.g. gradientBoosting)
	1. `cd gradientBoosting`
	2. build train-container `make build-train`
	3. run train-container `make train`
2.	### Model Predict
	1.	`cd gradientBoosting`
	2.	build predict-container `make build-predict`
	3.	run predict-container `make predict`

3. ### Run test:
	 1.	`cd gradientBoosting`
	 2.	`make test-endpoint`


## Build & Run all models together

1.	`cd all`
2.	to train all models `make train-all`
3.	to predict all models `make predict-all`
