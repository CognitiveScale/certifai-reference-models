.PHONY: setup-space test-all train-all-local
SHELL := /bin/bash

MODEL_DIRS := linearRegressionL1 linearRegressionL2 supportVectorRegression randomForest
CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
projectname := $(shell basename $(dir $(abspath $(dir pwd))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../
CONTAINER_NAME = 'auto-insurance-all'

setup-space:
	@mkdir -p .s2i/

test-all:
	@for dir in $(MODEL_DIRS) ; do \
		echo "testing ${CONTAINER_NAME} -"$$dir ; \
		cd ${PROJECT_ROOT_DIR}$$dir && make test-endpoint || exit 1; \
	done

train-all-local:
	@for dir in $(MODEL_DIRS) ; do \
		echo "training "$$dir locally; \
		cd ${PROJECT_ROOT_DIR}$$dir && make train-local || exit 1 ; \
	done
