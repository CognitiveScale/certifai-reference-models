
# Banking: Loan Approval(German Credit)

  In this use case, each entry in the [dataset](#Datasets) represents a person who takes a credit loan from a bank. Learning task is to classify each person as either a good or bad credit risk based on the set of attributes of that person. Model predicts whether loan will be _granted_ or _not-granted_ based on the credit risk evaluation. This dataset was sourced from [Kaggle](https://www.kaggle.com/uciml/german-credit). Originally from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data))


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
