SHELL := /bin/bash
.PHONY: build-train train build-predict predict test-endpoint

CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../

MODEL_NAME = "auto_insurance_linl2"
DATASET_NAME = "data/auto_insurance_claims_dataset.csv"
CONTAINER_NAME = 'auto-insurance-linl2'

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
