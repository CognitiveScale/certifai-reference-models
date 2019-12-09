
# Banking: Propensity to Buy (Bank Marketing)

In this use case, each entry in the dataset represents a target of a previous marketing campaign. earning task is to predict who will make a term deposit with the bank as a result of a similar campaign. This dataset was sourced from [Kaggle](https://www.kaggle.com/janiobachmann/bank-marketing-dataset). Originally from the [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Bank+Marketing))


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
