#!/bin/bash

CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../

MODEL_NAME = "auto_insurance_svr"
DATASET_NAME = "data/auto_insurance_claims_dataset.csv"
CONTAINER_NAME = 'auto-insurance-svr'

PAYLOAD = '{"$$ref": ${DATASET_NAME}, "model_name": ${MODEL_NAME} }'

build-train:
	cd ../ && sh build.sh ${CONTAINER_NAME}-train '$(CURRENT_DIR)' 'train'

train:
	cd ../ && docker run --rm  --rm  -v $(PROJECT_ROOT_DIR)/data:/model/data -v $(PROJECT_ROOT_DIR)/models:/model/models -e TRAIN=1 -e PAYLOAD=${PAYLOAD} -it --rm ${CONTAINER_NAME}-train

build-predict:
	cd ../ && sh build.sh ${CONTAINER_NAME}-predict '$(CURRENT_DIR)' 'predict'

predict:
	docker run --rm  --rm -v $(PROJECT_ROOT_DIR)/models:/action/models -e MODElNAME=${MODEL_NAME} -p 5111:5000 -it ${CONTAINER_NAME}-predict

test-endpoint:
	# endpoint from .s2i/environment ROUTES	 
	time http -v -j POST :5111/auto_insurance_svr/predict < test/test_instances.json

config:
	cat .s2i/environment