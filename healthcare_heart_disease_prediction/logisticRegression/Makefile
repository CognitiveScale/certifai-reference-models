SHELL := /bin/bash

CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../

MODEL_NAME = "heart_disease_lr"
DATASET_NAME = "data/heart_disease_multiclass-prepped.csv"
CONTAINER_NAME = 'heart-disease-lr'


PAYLOAD = '{"$$ref": ${DATASET_NAME}, "model_name": ${MODEL_NAME} }'

build-train:
	cd ../ && sh build.sh ${CONTAINER_NAME}-train '$(CURRENT_DIR)' 'train'

train:
	cd ../ && docker run --rm  -v $(PROJECT_ROOT_DIR)/data:/model/data -v $(PROJECT_ROOT_DIR)/models:/model/models -e TRAIN=1 -e PAYLOAD=${PAYLOAD} -it --rm ${CONTAINER_NAME}-train

build-predict:
	cd ../ && sh build.sh ${CONTAINER_NAME}-predict '$(CURRENT_DIR)' 'predict'

predict:
	docker run --rm  -v $(PROJECT_ROOT_DIR)/models:/action/models -e MODElNAME=${MODEL_NAME} -p 5111:5000 -it ${CONTAINER_NAME}-predict

test-endpoint:
	# endpoint from .s2i/environment ROUTES
	time http -v -j POST :5111/$(MODEL_NAME)/predict < test/test_instances.json

train-local: setup_local_space
	cd ../ && PYTHONPATH=.. python $(shell pwd | awk -F / '{print $$NF}')/train.py '{"payload": $(shell sed -e 's/^"//' -e 's/"$$//' <<< ${PAYLOAD})}'

predict-local:
	cd ../ && PYTHONPATH=.. python $(shell pwd | awk -F / '{print $$NF}')/predict.py $(shell cat .s2i/environment | grep -o -E 'ROUTES=[^ ]+' | sed -e 's/ROUTES=//')

help-local:
	@echo "make sure all dependencies are installed locally."
	@echo "all deps can be found at certifai-reference-models/all/requirements_local.txt"
	@echo "to install deps from file requirements_local.txt run "
	@echo "pip install -r requirements_local.txt"

setup_local_space:
	@mkdir -p ../models
