# Adding ML Models to Projects

To add models to available projects:-
1. create a model dir (e.g logisticRegression, catboost etc.) inside the project of your choice
2. add a training module (e.g train.py) and a predict module (eg. predict.py)
3. to add train and predict dependencies create files named `requirements_train.txt` and `requirements_predict.txt` respectively in the model directory created above
   > note dependencies are installed using pip
4. additional native dependencies can be installed with a `setup.sh` script present at the root level in the model directory. 
> `setup.sh` is executed before installing other code dependencies mentioned in <requirements_.txt>
5. train && predict(service routes) configurations are handled using an .s2i/environment file. To create such a config add a `.s2i/environment` file at the root level model directory
6. structure of `.s2i/environment` file

```
ROUTES=serviceroute:predictModule:predictFunction
TRAIN_MODULE=<module containing train.py>
TRAIN_FUNCTION=<function to invoke to start model training>
```

7. to build the training container we use s2i(source-to-image) with a base container with minimal dependencies(e.g. python3). Refer to [s2i-docs](https://github.com/openshift/source-to-image]) for further study
> `s2i build -c . c12e/cortex-s2i-model-python36-slim:1.0-SNAPSHOT <TRAIN_CONTAINER_NAME>`

> `c12e/cortex-s2i-model-python36-slim:1.0-SNAPSHOT` is the base image as discussed above



8. to run the training container:
>  `docker run --rm  -v $(PROJECT_ROOT_DIR)/data:/model/data -v $(PROJECT_ROOT_DIR)/models:/model/models -e TRAIN=1 -e PAYLOAD=${PAYLOAD} -it --rm ${TRAIN_CONTAINER_NAME}`

> here we use volume mounts(-v) to persist files(model_binaries,data etc.) on disk

9. to build the predict container: 
> `s2i build -c . c12e/cortex-s2i-daemon-python36-slim:1.0-SNAPSHOT ${PREDICT_CONTAINER_NAME}`

10. to run the predict container:
> `docker run --rm  -v $(PROJECT_ROOT_DIR)/models:/action/models -e MODElNAME=${MODEL_NAME} -p 5111:5000 -it ${PREDICT_CONTAINER_NAME}`

## Code Organization

### finance_income_prediction (e.g.)
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

#### In the above e.g. we have 3 sample models namely logisticRegression, randomForest and xgBoost to predict adult income given individual features like education levels, gender, job description etc. 

> files pre-fixed with * are auto-generated 

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




