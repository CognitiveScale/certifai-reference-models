# Healthcare: Heart Disease Prediction

**Learning Task Type**: Multiclass Classification

**Description**: In this use case, each entry in the dataset represents a patient. The models predict whether or not a patient has heart disease (angiographic disease status).

**Dataset Source**: [UCI Machine Learning Repository](http://archive.ics.uci.edu/ml/datasets/Heart+Disease)

**Pre-Trained Model**:

  - Logistic Regression
  - Random Forest
  - K Nearest Neighbors

**Evaluation Types**:

  - Robustness
  - Fairness
  - Explainability
  - Explanations

# Prerequisites

1. [Source-to-Image](https://github.com/openshift/source-to-image)
2. Make (Program building utility available by default with Linux and MacOS; for Windows use GNUWin32)
3. [Httpie](https://httpie.org/) (Required to run `make test-endpoint`)


## Train, Predict, and Test Use Case Models Individually

Follow the instructions to train, predict, and test each model individually.

1\. Model train (e.g. logisticRegression)

 - a. Go to the use-case/model directory.  - `cd useCase/modelName` Example: `cd healthcare_heart_disease_prediction/logisticRegression`
 - b. Create a Docker image to train the models. -  `make build-train`
 - c. Run the Docker image created above as a container to train the model and produce the model_binary. - `make train`

2\. Model predict

 - a. Go to the use-case/model directory. - `cd useCase/modelName` Example: `cd healthcare_heart_disease_prediction/logisticRegression`
 - b. Create the Docker image to expose predict branch of the trained model as a web service api. -  `make build-predict`
 - c. Runs the Docker image created above as a container to start the server. After this step, the server can be invoked to obtain predictions. -  `make predict`

3\. Run test

 - a. Go to the use-case/model directory - `cd useCase/modelName` Example: `cd healthcare_heart_disease_prediction/logisticRegression`
 - b. Test the web server by passing it a single record as json. The test returns a model prediction. - `make test-endpoint`

## Train, Predict, and Test Use Case Models Together

Follow the instructions to train, predict, and test all the models for the use case at the same time.

1. Go to the useCase/all directory - `cd useCase/all` Example: `cd healthcare_heart_disease_prediction/all`
2. Train all models -  `make train-all`
3. Predict all models -  `make predict-all`
