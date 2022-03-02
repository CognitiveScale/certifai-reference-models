.PHONY: setup-build-space train-projects-all-local create-routes-all test-all-endpoints help-local

SHELL := /bin/bash

MODEL_DIRS := bank_marketing banking_customer_churn_prediction banking_loan_approval finance_income_prediction healthcare_disease_prediction insurance_auto_insurance_claims healthcare_heart_disease_prediction
CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../
CONTAINER_NAME = 'c12e/certifai-reference-models-server'

setup-build-space:
	mkdir -p ${PROJECT_ROOT_DIR}/models
	rm -rf ${PROJECT_ROOT_DIR}/models/*
	mkdir -p .s2i/

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
		cd ${PROJECT_ROOT_DIR}$$dir/all && make test-all || exit 1 ; \
		sleep .5 ; \
	done

train-projects-all-local:
	@for dir in $(MODEL_DIRS) ; do \
		echo "Building "$$dir ; \
		cd ${PROJECT_ROOT_DIR}$$dir/all && make train-all-local || exit 1 ; \
	done

help-local:
	@echo "make sure all dependencies are installed locally."
	@echo "all deps can be found at certifai-reference-models/all/requirements_local.txt"
	@echo "to install deps from file requirements_local.txt run "
	@echo "pip install -r requirements_local.txt"
