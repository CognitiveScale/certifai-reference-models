.PHONY: setup-build-space train-projects-all predict-projects-all create-routes-all test-all-endpoints run-model-server

SHELL := /bin/bash

MODEL_DIRS := bank_marketing banking_customer_churn_prediction banking_loan_approval finance_income_prediction healthcare_disease_prediction insurance_auto_insurance_claims
CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../
CONTAINER_NAME = 'c12e/model-server'

setup-build-space:
	mkdir -p ${PROJECT_ROOT_DIR}/models
	rm -rf ${PROJECT_ROOT_DIR}/models/*
	mkdir -p .s2i/

train-projects-all:
	@for dir in $(MODEL_DIRS) ; do \
		echo "Building "$$dir ; \
		cd ${PROJECT_ROOT_DIR}$$dir/all && make train-all ; \
	done

build-container:
	@mkdir -p ${PROJECT_ROOT_DIR}/build-context
	@rm -rf ${PROJECT_ROOT_DIR}/build-context/
	rsync -av --exclude=/.git* --exclude=/data --exclude=/build-context --delete-excluded  ${PROJECT_ROOT_DIR}/ ${PROJECT_ROOT_DIR}/all/ ${PROJECT_ROOT_DIR}/build-context
	rsync -avr --include="setup.sh" --exclude="*" ${PROJECT_ROOT_DIR}/**/**/ ${PROJECT_ROOT_DIR}/build-context
	s2i build --rm -c ${PROJECT_ROOT_DIR}/build-context c12e/cortex-s2i-daemon-python36-slim:1.0.0 ${CONTAINER_NAME}
	# remove build artifacts
	rm -rf ${PROJECT_ROOT_DIR}/build-context


predict-projects-all: create-routes-all build-container
	docker run --rm -v $(PROJECT_ROOT_DIR)/models:/action/models -p 5111:5000 -it ${CONTAINER_NAME}

create-routes-all: setup-build-space
	@echo  "ROUTES=" | tr -d "\n" > .s2i/env
	@for dir in $(MODEL_DIRS) ; do \
		cd ${PROJECT_ROOT_DIR}$$dir && cp -r models/*  ${PROJECT_ROOT_DIR}/models/ ; \
		cd all/ && make create-routes ; \
		cat .s2i/environment | grep -o -E 'ROUTES=[^ ]+' | sed -e 's/ROUTES=//' | sed -e 's/$$/,/' | tr -d '\n' >> ${CURRENT_DIR}/.s2i/env  ; \
	done
	@(cat .s2i/env | sed 's/.$$//') | tee .s2i/environment
	rm -f .s2i/env

test-all-endpoints:
	@for dir in $(MODEL_DIRS) ; do \
		echo "testing "$$dir ; \
		cd ${PROJECT_ROOT_DIR}$$dir/all && make test-all ; \
		sleep .5 ; \
	done

run-model-server:
	docker run --rm -v $(PROJECT_ROOT_DIR)/models:/action/models -p 5111:5000 -it ${CONTAINER_NAME}

train-projects-all-local:
	@for dir in $(MODEL_DIRS) ; do \
		echo "Building "$$dir ; \
		cd ${PROJECT_ROOT_DIR}$$dir/all && make train-all-local ; \
	done

predict-projects-all-local: help-local create-routes-all
	cd ../ && PYTHONPATH=. python ${PROJECT_ROOT_DIR}/utils/local_server.py $(shell cat .s2i/environment | grep -o -E 'ROUTES=[^ ]+' | sed -e 's/ROUTES=//')

help-local:
	@echo "make sure all dependencies are installed locally."
	@echo "all deps can be found at certifai-reference-models/all/requirements_local.txt"
	@echo "to install deps from file requirements_local.txt run "
	@echo "pip install -r requirements_local.txt"


train-pipeline: train-projects-all-local
	@for dir in $(MODEL_DIRS) ; do \
		cd ${PROJECT_ROOT_DIR}$$dir && cp -r models/*  ${PROJECT_ROOT_DIR}/models/ ; \
	done

run-pipeline: create-routes-all build-container
	@echo starting train inside container
	docker run --rm -it -v $(PROJECT_ROOT_DIR)/models:/action/models  --entrypoint '/bin/bash' ${CONTAINER_NAME}  -c 'cd all && make train-pipeline && exit 0'
	@echo starting predict container
	docker run --rm -v $(PROJECT_ROOT_DIR)/models:/action/models -p 5111:5000 -it ${CONTAINER_NAME}