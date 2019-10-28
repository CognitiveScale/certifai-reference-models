.PHONY: help run docker-build docker-run install train train-diabetes train-german train-auto train-bank train-customer

CONDA_PYTHON_PATH := $(shell conda env list | grep "/model-server$$" | awk '{print $$NF}' | xargs -I {} echo "{}/bin/")
DOCKER_INTERNAL_PORT = 5000
ROOT_DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
THIS_MAKE_FILE := $(lastword $(MAKEFILE_LIST))
EXAMPLES_DIR := examples

help: ## Prints help for targets with comments
	@echo 'Make targets:'
	@grep -E '^[a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: ## runs the model server
	$(CONDA_PYTHON_PATH)python -m model_server

docker-build: train ## build the docker image used for the model server (after training all models)
	s2i build . c12e/cortex-s2i-daemon-python36-slim:1.0-SNAPSHOT example-models-daemon

docker-run: ## runs the model server from a docker container
	docker run -p 8551:${DOCKER_INTERNAL_PORT} example-models-daemon

install: ## installs pip requirements
	$(CONDA_PYTHON_PATH)/pip install -r requirements.txt

# TODO(la): use a loop here?
train: ## trains all existing models
	# the || true makes it keep building when previous failed
	@$(MAKE) -f $(THIS_MAKE_FILE) train-diabetes || true
	@$(MAKE) -f $(THIS_MAKE_FILE) train-german || true
	@$(MAKE) -f $(THIS_MAKE_FILE) train-auto || true
	@$(MAKE) -f $(THIS_MAKE_FILE) train-bank || true
	@$(MAKE) -f $(THIS_MAKE_FILE) train-customer || true
	@$(MAKE) -f $(THIS_MAKE_FILE) train-telco || true
	@$(MAKE) -f $(THIS_MAKE_FILE) train-heart || true
	@$(MAKE) -f $(THIS_MAKE_FILE) train-adult || true

train-diabetes:  ## trains diabetes models
	cd $(EXAMPLES_DIR)/diabetes; rm -rdf models/; mkdir models; $(CONDA_PYTHON_PATH)python make_diabetes_models.py

train-german: ## trains german_credit models
	cd $(EXAMPLES_DIR)/german_credit; rm -rdf models/; mkdir models; $(CONDA_PYTHON_PATH)python make_german_decoded_models.py

train-auto: ## trains auto_insurance models
	cd $(EXAMPLES_DIR)/auto_insurance; rm -rdf models/; mkdir models; $(CONDA_PYTHON_PATH)python make_auto_insurance_models.py

train-bank: ## trains bank_marketing models
	cd $(EXAMPLES_DIR)/bank_marketing; rm -rdf models/; mkdir models; $(CONDA_PYTHON_PATH)python make_bank_marketing_models.py

train-customer: ## trains customer churn models
	cd $(EXAMPLES_DIR)/customer_churn; rm -rdf models/; mkdir models; $(CONDA_PYTHON_PATH)python make_customer_churn_models.py

train-telco: ## trains telco customer churn models
	cd $(EXAMPLES_DIR)/telco_customer_churn; rm -rdf models/; mkdir models; $(CONDA_PYTHON_PATH)python make_telco_customer_churn_models.py

train-adult: ## trains adult income prediction model
	cd $(EXAMPLES_DIR)/adult_income; rm -rdf models/; mkdir models; $(CONDA_PYTHON_PATH)python make_adult_income_prediction_models.py

train-heart: ## trains heart disease multiclass prediction models
	cd $(EXAMPLES_DIR)/heart_disease_multiclass; rm -rdf models/; mkdir models; $(CONDA_PYTHON_PATH)python make_heart_disease_multiclass_models.py
