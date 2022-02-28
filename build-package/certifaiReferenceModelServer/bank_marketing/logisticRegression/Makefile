SHELL := /bin/bash
.PHONY: setup_local_space train-local test-endpoint

CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../

MODEL_NAME = "bank_marketing_logit"
DATASET_NAME = "data/bank_marketing-prepped.csv"
CONTAINER_NAME = 'bank-marketing-logit'

PAYLOAD = '{"$$ref": ${DATASET_NAME}, "model_name": ${MODEL_NAME} }'

test-endpoint:
	curl --fail -X POST -H "Content-Type: application/json" \
	  -d @test/test_instances.json ":5111/${MODEL_NAME}/predict"

train-local: setup_local_space
	cd ../ && PYTHONPATH=.. python $(shell pwd | awk -F / '{print $$NF}')/train.py '{"payload": $(shell sed -e 's/^"//' -e 's/"$$//' <<< ${PAYLOAD})}'

setup_local_space:
	@mkdir -p ../models
