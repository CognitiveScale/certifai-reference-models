# Insurance: Auto Insurance Claims(auto insurance)

**Learning Task Type**: Regression

**Description**: Each dataset row represents the attribute values for an auto insurance claim. The models predict the final claim settlement amount.

**Dataset Source**: [Emcien](https://www.sixtusdakurah.com/resources/The_Application_of_Regularization_in_Modelling_Insurance_Claims.pdf)

**Pre-trained Models**:

  - L1 Linear Regression
  - L2 Linear Regression
  - Neural Network
  - Random Forest Regressor
  - SVR

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
1. ### Model train (e.g. linearRegressionL1)
	1. `cd linearRegressionL1`
	2. build train-container `make build-train`
	3. run train-container `make train`
2.	### Model Predict
	1.	`cd linearRegressionL1`
	2.	build predict-container `make build-predict`
	3.	run predict-container `make predict`

3. ### Run test:
	 1.	`cd linearRegressionL1`
	 2.	`make test-endpoint`


## Build & Run all models together

1.	`cd all`
2.	to train all models `make train-all`
3.	to predict all models `make predict-all`
