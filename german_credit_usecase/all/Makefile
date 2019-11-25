#!/bin/bash

MODEL_DIRS := logisticRegression decisionTree multiLayerPerceptron supportVectorMachine
CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../
CONTAINER_NAME = 'german-credit-all'

train-all:
	@for dir in $(MODEL_DIRS) ; do \
		echo "Building "$$dir ; \
		cd ${PROJECT_ROOT_DIR}$$dir && make build-train && make train ; \
	done

predict-all: create-routes
		@mkdir -p ${PROJECT_ROOT_DIR}/build-context
		@rm -rf ${PROJECT_ROOT_DIR}/build-context/
		rsync -av --exclude=/data --exclude=/build-context --exclude=/models --exclude=all ${PROJECT_ROOT_DIR} ${PROJECT_ROOT_DIR}/all/ ${PROJECT_ROOT_DIR}/build-context		
	    s2i build -c ${PROJECT_ROOT_DIR}/build-context c12e/cortex-s2i-daemon-python36-slim:1.0-SNAPSHOT ${CONTAINER_NAME}
		# remove build artifacts
		rm -rf ${PROJECT_ROOT_DIR}/build-context
		docker run -v $(PROJECT_ROOT_DIR)/models:/action/models -p 5111:5000 -it ${CONTAINER_NAME}

create-routes:
	echo  "ROUTES=" | tr -d "\n" > .s2i/environment  
	@for dir in $(MODEL_DIRS) ; do \
		cd ${PROJECT_ROOT_DIR}$$dir && cat .s2i/environment | grep -o -E 'ROUTES=[^ ]+' | sed -e 's/ROUTES=//' | sed -e 's/$$/,/' | tr -d '\n' >> ${CURRENT_DIR}/.s2i/environment  ; \
	done
	(cat .s2i/environment | sed 's/.$$//' ; echo "PREDICT_MODULE=predict") | tee .s2i/environment