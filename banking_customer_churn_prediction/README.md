
# Banking: Predicting Customer Churn

In this use case, each entry in the dataset represents a customer or previous customer of the bank. Learning task is to predict who is likely to quit as a customer. This dataset was sourced from [Kaggle](https://www.kaggle.com/adammaus/predicting-churn-for-bank-customers


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
