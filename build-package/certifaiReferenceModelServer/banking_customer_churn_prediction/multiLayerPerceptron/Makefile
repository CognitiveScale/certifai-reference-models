SHELL := /bin/bash

CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../

MODEL_NAME = "customer_churn_mlp"
DATASET_NAME = "data/customer_churn-prepped.csv"
CONTAINER_NAME = 'customer-churn-mlp'


PAYLOAD = '{"$$ref": ${DATASET_NAME}, "model_name": ${MODEL_NAME} }'

test-endpoint:
	curl --fail -X POST -H "Content-Type: application/json" \
	  -d @test/test_instances.json "0.0.0.0:5111/${MODEL_NAME}/predict"

train-local: setup_local_space
	cd ../ && PYTHONPATH=.. python $(shell pwd | awk -F / '{print $$NF}')/train.py '{"payload": $(shell sed -e 's/^"//' -e 's/"$$//' <<< ${PAYLOAD})}'

predict-local:
	cd ../ && PYTHONPATH=.. python $(shell pwd | awk -F / '{print $$NF}')/predict.py

setup_local_space:
	@mkdir -p ../models
