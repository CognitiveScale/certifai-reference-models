
# Finance: Income Prediction 

**Learning Task Type**: Binary Classification

**Description**: Each dataset row represents the attribute values for de-identified individual. The models predict the income tax bracket of the person as `<=50K` or `>=50 K`.

**Dataset Source**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/census+income)

**Pre-trained Models**:

  - SVM
  - Random Forest
  - XGBoost

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
1. ### Model train (e.g. logisticRegression)
	1. `cd logisticRegression`
	2. build train-container `make build-train`
	3. run train-container `make train`
2.	### Model Predict
	1.	`cd logisticRegression`
	2.	build predict-container `make build-predict`
	3.	run predict-container `make predict`

3. ### Run test:
	 1.	`cd logisticRegression`
	 2.	`make test-endpoint`


## Build & Run all models together

1.	`cd all`
2.	to train all models `make train-all`
3.	to predict all models `make predict-all`
