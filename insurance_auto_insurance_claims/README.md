
# Insurance: Auto Insurance Claims(auto insurance)

 In this use case, each entry in the dataset represents an auto insurance claim. Learning task is to predict the final settled claim amount. This dataset was sourced from [Emcien](https://www.sixtusdakurah.com/resources/The_Application_of_Regularization_in_Modelling_Insurance_Claims.pdf)

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
