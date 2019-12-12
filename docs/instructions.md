# Adding ML Models to Projects

To add models to available projects:

1. Create a model directory inside your project (e.g logisticRegression, catboost etc.).

2. Add a training module (e.g train.py) and a predict module (eg. predict.py).

3. Add train and predict dependencies by creating files named `requirements_train.txt` and `requirements_predict.txt` respectively in the model directory created above.

   **NOTE**: Dependencies are installed using `pip`.

4. Install additional native dependencies with a `setup.sh` script present at the root-level in the model directory.

  `setup.sh` is executed before installing other code dependencies defined in the `requirements.txt` file.

5. Train & predict configurations (service routes) are handled using an .s2i/environment file. To create service routes configurations, add an `.s2i/environment` file at the root level of your model directory. Structure the `.s2i/environment` file as follows:

  ```
  ROUTES=serviceroute:predictModule:predictFunction
  TRAIN_MODULE=<module containing train.py>
  TRAIN_FUNCTION=<function to invoke to start model training>
  ```

7. Build the training container using the s2i (source-to-image) with a base container with minimal dependencies (e.g. python3). Refer to [s2i-docs](https://github.com/openshift/source-to-image]) for more information.

 ```
 s2i build -c . c12e/cortex-s2i-model-python36-slim:1.0-SNAPSHOT <TRAIN_CONTAINER_NAME>
 ```

  The base image as discussed above is `c12e/cortex-s2i-model-python36-slim:1.0-SNAPSHOT`.

8. Run the training container using volume mount (-v) to persist files (model_binaries, data etc.) on disk.

  ```
  docker run --rm  -v $(PROJECT_ROOT_DIR)/data:/model/data -v $(PROJECT_ROOT_DIR)/models:/model/models -e TRAIN=1 -e PAYLOAD=${PAYLOAD} -it --rm ${TRAIN_CONTAINER_NAME}
  ```

9. Build the predict container.

  ```
  s2i build -c . c12e/cortex-s2i-daemon-python36-slim:1.0-SNAPSHOT ${PREDICT_CONTAINER_NAME}
  ```

10. Run the predict container.

  ```
  docker run --rm  -v $(PROJECT_ROOT_DIR)/models:/action/models -e MODElNAME=${MODEL_NAME} -p 5111:5000 -it ${PREDICT_CONTAINER_NAME}
  ```

## Model Predict: Request/Response

The predict endpoint takes an array of instances containing an array of feature values.
```
curl -X POST \
 http://localhost:5111/<route> \
 -H 'Content-Type: application/json' \
 -d '{
"payload": { "instances": [[7,107,74,0,0,29.6,0.254,31]] }
}'
```
`route` is defined using .s2i/environment file

It returns an array of predictions.
```
{
   "payload": {
     "predictions": [1]
   }
}
```

Sample example predict for the bank_marketing:

`REQUEST`

```
curl -X POST \
  http://localhost:5111/bank_marketing_logit/predict  \
  -H 'Content-Type: application/json' \
  -d '{
      "payload": {
		"instances": [
			"age_25_or_above",
			"job_admin.",
			"marital_married",
			"education_secondary",
			"default_no",
			2343,
			"housing_yes",
			"loan_no",
			"contact_unknown",
			"month_may",
			1042,
			1,
			-1,
			0,
			"poutcome_unknown"
		]
      }
}'
```
`RESPONSE`

```
{"payload":{"predictions":[1]}}
```



## Code Organization Example

finance_income_prediction

```
├── README.md
├── all
│   ├── .s2i
│   │   └── *environment
│   ├── Makefile
│   ├── predict.py
│   ├── requirements.txt
│   └── setup.sh
├── build.sh
├── common_utils
│   ├── __init.py__
│   └── train_utils.py
├── data
│   └── adult_income-prepped.csv
├── logisticRegression
│   ├── .s2i
│   │   └── environment
│   ├── Makefile
│   ├── README.md
│   ├── __init__.py
│   ├── predict.py
│   ├── requirements_predict.txt
│   ├── requirements_train.txt
│   ├── test
│   │   └── test_instances.json
│   └── train.py
├── models
│   ├── *adult_income_lr.pkl
│   ├── *adult_income_rf.pkl
│   └── *adult_income_xgb.pkl
├── randomForest
│   ├── .s2i
│   │   └── environment
│   ├── Makefile
│   ├── README.md
│   ├── predict.py
│   ├── requirements_predict.txt
│   ├── requirements_train.txt
│   ├── test
│   │   └── test_instances.json
│   └── train.py
└── xgBoost
    ├── .s2i
    │   └── environment
    ├── Makefile
    ├── README.md
    ├── predict.py
    ├── requirements_predict.txt
    ├── requirements_train.txt
    ├── setup.sh
    ├── test
    │   └── test_instances.json
    └── train.py
```

In the finance_income_prediction example the three sample models, logisticRegression, randomForest, and xgBoost, predict adult income given features like education level, gender, and job description. 

  **NOTE**: Files pre-fixed with * are auto-generated.

## Common

At the root level we define modules which are to be used across all the models for instance `common_utils.train_utils.py`, `data/adult_income-prepped.csv` etc.

Even directories common to all projects can be included like `utils` which includes functions to  encode-decode model binaries for all models and all projects

## build.sh

Similarily, `build.sh` at top-level dir helps us customize files, folders, artifacts that we want to include in the container.

This gives us enough flexibility as well as power to structure the content as and how we want. It also includes the `s2i` base images that are used as builders for train and predict.

Regular users can use the default setup that comes with `build.sh`.

## Makefile

Each model (e.g randomForest) dir also consists of a  `Makefile` that has commands to build and run the containers.

User needs to sepcify:

1. MODEL_NAME: model binary will be saved with this name e.g. `adult_income_rf` will save the model as `adult_income_rf.pkl` in the models dir

2. DATASET_NAME: data to be used for training the model. for e.g. `data/adult_income-prepped.csv` will look for file named `adult_income-prepped.csv` in common data directory discussed above

3. CONTAINER_NAME: name of the container containing the train or predict functionality. e.g. `adult-income-rf` will create containers named `adult-income-rf-train` and `adult-income-rf-predict` for the train and predict respectively


Makefile Commands:

1.  `make build-train`: builds train container
2.  `make train`: runs the train container, generates model binary'
3.  `make build-predict`: builds the predict container
4.  `make predict`: runs the predict container and exposes model's predict as a web-service endpoint
5.  `make test-endpoint`: test's the model's predict endpoint using a data instances defined in test/test_instances.json


## s2i

Each model needs to have an `.s2i/environment` file which defines the routes to create to expose model's predict method.

e.g.

```
ROUTES=adult_income_rf/predict:finance_income_prediction.predict:predict_adult_income_rf
TRAIN_MODULE=finance_income_prediction.train
TRAIN_FUNCTION=train
PREDICT_MODULE=finance_income_prediction.predict
PREDICT_FUNCTION=predict_adult_income_rf
```

1.  ROUTES: defines endpoint to create and function to call when endpoint is invoked
`serviceroute:predict-module-name:predict-function-name`
2. TRAIN_MODULE: defines python module in which train function is defined
3. TRAIN_FUNCTION: train function name
4.  PREDICT MODULE AND PREDICT FUNCTION: same as train but for predict.

> in case of using daemon s2i builder we only need to specify ROUTES.
PREDICT_MODULE && PREDICT FUNCTION are optional when using `s2i` daemon builder image. Though we  provide it in all our examples for readability

here:

`adult_income_rf/predict` is the web-service route
`finance_income_prediction.predict` is the python module in which predict functionality is defined
`predict_adult_income_rf` is the predict function name defined in the `finance_income_prediction.predict` module shown above


## all

All models can be trained and packaged together as well, exposing predict for an entire project/usecase(with 3 models here) as one single container with multiple routes for each of those models.

> note `all` creates a new predict container with all routes in exactly the same way as individual models are created. Hence it needs the same files, some of which like .s2i/environment can be auto generated


`training` here just invokes the individual model's train functionality. no sepate train module needed.

`prediction` here needs a predict module with just the correct function imports from individual model dirs to invoke the correct method when called with that endpoint. (TODO: automate predict.py using code gen)

`requirements.txt`  list of pip installable modules
required when creating single container with all models

Here the `.s2i/environment` is auto-generated from individual model's .s2i/environment files defined inside each of the container

Here user needs to specify:

1.  MODEL_DIRS := xgBoost logisticRegression randomForest
    for the model dirs to include in the container
2. CONTAINER_NAME: name of the predict container containing all routes

`make train-all`: trains all models defined in model dirs

`make predict-all`: starts the predict container with all the models loaded and serves them as web service routes

`make test-all`:  invokes the predict for each of the models against the predict-all container using test defined in each model
