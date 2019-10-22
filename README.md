# Overview

This directory contains a simple flask app to serve up pickled models. By default it runs on port 8551.

It also contains the metadata needed to build a docker container to serve the models using s2i.

## Predict

The predict endpoint takes an array of instances containing an array of feature values.
```
curl -X POST \
 http://localhost:8551/<model_name>/predict \
 -H 'Content-Type: application/json' \
 -d '{
"payload": { "instances": [[7,107,74,0,0,29.6,0.254,31]] }
}'
```
The `<model_name>` must be a pickled model in the models directory, for example `diabetes_svm`.

It returns an array of predictions.
```
{
   "payload": {
     "predictions": [1]
   }
}
```

An example predict for the German Credit example is:

```
curl -X POST \
  http://localhost:8551/german_credit_logit/predict \
  -H 'Content-Type: application/json' \
  -d '{
  "payload": {
    "instances": [ ["... < 0 DM", 6, "critical account/ other credits existing (not at this bank)", "radio/television", 1169, "unknown/ no savings account", ".. >= 7 years", 4, "male : single", "others - none", 4, "real estate", "> 25 years", "none", "own", 2, "skilled employee / official", 1, "phone - yes, registered under the customers name", "foreign - yes"],
    ["0 <= ... < 200 DM", 48, "existing credits paid back duly till now", "radio/television", 5951, "... < 100 DM", "1 <= ... < 4 years", 2, "female : divorced/separated/married", "others - none", 2, "real estate", "> 25 years", "none", "own", 1, "skilled employee / official", 1, "phone - none", "foreign - yes"],
    ["no checking account", 12, "critical account/ other credits existing (not at this bank)", "education", 2096, "... < 100 DM", "4 <= ... < 7 years", 2, "male : single", "others - none", 3, "real estate", "> 25 years", "none", "own", 1, "unskilled - resident", 2, "phone - none", "foreign - yes"],
    ["... < 0 DM", 42, "existing credits paid back duly till now", "furniture/equipment", 7882, "... < 100 DM", "4 <= ... < 7 years", 2, "male : single", "guarantor", 4, "building society savings agreement/ life insurance", "> 25 years", "none", "for free", 1, "skilled employee / official", 2, "phone - none", "foreign - yes"]]
  }
}'
```

## Models

### `Examples` folder Structure
All examples (e.g. auto_insurance, bank_marketing, etc.) can be found in the
`examples` directory. Each use case should have its own subdirectory with its
source code, any related datasets in a `data` directory, and any pickled models
in the `models` directory.

**NOTE: The `models/` directory and pickle files are not pushed to the git repo
anymore, to create them locally look [here](#training-existing-models)**

```
├─ examples
│  ├── auto_insurance
│  │   ├── __init__.py
│  │   ├── auto_insurance_encoder.py
│  │   ├── make_auto_insurance_models.py
│  │   ├── data/
│  │   └── models/
│  ├── bank_marketing
│  │   ├── __init__.py
│  │   ├── bank_marketing_encoder.py
│  │   ├── make_bank_marketing_models.py
│  │   ├── data/
│  │   └── models/
```

The examples should be setup to read data from the `data` directory for training, create pickle files in the `models` directory,
and write a `performance_metrics.csv` file in `models` directory with information about the models in csv format. The format is currently in the form:
```
Model,<Performance-Metric-Name>
<model-name>,<performance_metric-value>
```

The performance metrics file should be created whenever we train the model. The existing binary-classification models have been using `Accuracy` as their performance metric, but the metric may vary per model.

The naming convention we are following for models is: `<example>_<model_type>.pkl`.
For example, a decision tree model for the diabetes example should be named `diabetes_dtree.pkl` and can be found at: `examples/diabetes/models/diabetes_dtree.pkl`.

## Training Existing Models

To train all existing models you can do:

```
conda activate model-server
make train
```

You can train an individual model by performing `make train-<example>`, such as `make train-diabetes`. Refer to `make help` to see the invidual commands.

## Adding a new Example

An example will consist of: datasets, source code for training and pickling models, and the pickle files.

When adding a new example:
 * Create a new directory under `examples`
 * Place your source code at the top level of the new directory
 * Set a constant random seed inside your code to make sure that the models will be deterministic between trainings (e.g use `random.seed()` and `np.random.seed()`)
 * Place any dataset (csv) files inside a `data` directory
 * Make sure pickled models will be written to the `models` directory
 * Make sure a `performance_metrics.csv` file will be written to the `models` directory
 * Follow the existing naming conventions for pickled models
 * Update the Makefile with a new target to train your model

If you follow the existing file structure and naming convention, then the model_server should be able to find any pickled models. You may run into file path issues when you attempt to run the model_server and invoke the models.

In order to make sure that the docker image running the `model_server` is updated, you will need to create prediction functions for each new model, and update the `.s2i/environment` with a new route for each model being added.

Create a new prediction function for each new model in `s2i_predict.py`. You can follow the general template of the existing functions.

Refer to [here](#adding-a-new-route-to-the-docker-container) for how to update the `.s2i/enviornment` file. The handler function you specify should be what you added in `s2i_predict.py`.

**NOTE:** The name of your pickled model will need to correspond with the expected route for invoking the model. For example, the sending a request to `http://localhost:5000/diabetes_svm/predict` will cause the model_server to invoke `examples/diabetes/models/diabetes_svm.pkl`.

## Running the flask app

Set up the conda environment:
```
conda env update -f environment.yaml
conda activate model-server
```

Run the app:
```
python -m model_server
```

Or:
```
make run
```

Pickled models are in `examples/<example>/models` and named named `<model_name>.pkl`.




## Building and running the docker container

You need to install [s2i](https://github.com/openshift/source-to-image). We are
using the the s2i tool with the `c12e/cortex-s2i-daemon-python36-slim:1.0-SNAPSHOT` builder image.

From the `model_server` folder, you can build the docker container using:

```
make docker-build
```

This will build an image called `example-models-daemon` which is a valid Cortex daemon. It can be
run using:

```
make docker-run
```

## Adding a new route to the docker container

We are using s2i tool with the `c12e/cortex-s2i-daemon-python36-slim:1.0-SNAPSHOT` builder image to host the models from inside a docker container.

To add a new route to the docker container, you will need to update `.s2i/environment` file and add a new predict function to the `s2i_predict.py`.

The `.s2i/environment` file defines a ROUTES variable with comma seperated entries describing
each route the server accepts and what function should respond to that route.
Update the ROUTES variable by appending the new route entry to the end (don't leave a trailing comma at the end).

The entries are separated by commas and consist of `<path>:<module>:<function>`. For example,
`diabetes_svm/predict:s2i_predict:predict_diabetes_svm` creates an endpoint at `diabetes_svm/predict`
which calls the `predict_diabetes_svm` function in `s2i_predict.py`.
