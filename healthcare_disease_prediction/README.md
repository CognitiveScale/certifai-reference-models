
# HealthCare: Disease Prediction(Diabetes)

In this use case, each entry in the dataset represents a patient. Learning task is to predict whether or not a patient has diabetes, based on certain diagnostic measurements included in the dataset. Several constraints were placed on the selection of these instances from a larger database. In particular, all patients here are females at least 21 years old of Pima Indian heritage. This dataset was sourced from [Kaggle](https://www.kaggle.com/uciml/pima-indians-diabetes-database ). Originally from the [National Institute of Diabetes and Digestive and Kidney Diseases](https://www.niddk.nih.gov/)

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
