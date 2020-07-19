.PHONY: setup-build-space train-projects-all build_package test

SHELL := /bin/bash

MODEL_DIRS := banking_loan_approval2
# MODEL_DIRS := bank_marketing banking_customer_churn_prediction banking_loan_approval finance_income_prediction healthcare_disease_prediction insurance_auto_insurance_claims healthcare_heart_disease_prediction
CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../

setup-build-space:
	mkdir -p models && mkdir -p dist
	rm -rf models/* dist/*
	rm -rf cortex_certifai_reference_model_server.egg-info
	pip uninstall cortex-certifai-reference-model-server -y
	find . -name __pycache__ -type d -exec rm -fr {} \; || true

train-projects-all:
	@for dir in $(MODEL_DIRS) ; do \
		echo "Building "$$dir ; \
		cd ${PROJECT_ROOT_DIR}$$dir && python train.py ; \
		find . -type f -name '*.pkl' -exec cp {} ${CURRENT_DIR}/certifaiReferenceModelServer/models/ \; ; \
	done;

build-package: setup-build-space train-projects-all
	sh build.sh

test:
	echo "starting server"
	if [ -f server.pid ]; then kill `cat server.pid` 2> /dev/null || true; fi
	{ python ${CURRENT_DIR}/certifaiReferenceModelServer/composed_app.py & echo $$! > server.pid; } ; \
	sleep 2 ;
	@for dir in $(MODEL_DIRS) ; do \
		echo "Testing "$$dir ; \
		python ${PROJECT_ROOT_DIR}$$dir/all/test_composed_app.py ; \
	done;
	kill `cat server.pid` && rm server.pid



