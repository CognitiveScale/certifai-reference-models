.PHONY: train-all predict-all create-routes test-all
SHELL := /bin/bash

MODEL_DIRS := logisticRegression
CURRENT_DIR := $(dir $(abspath $(firstword $(MAKEFILE_LIST))))
projectname := $(shell basename $(dir $(abspath $(dir pwd))))
PROJECT_ROOT_DIR := $(CURRENT_DIR)../
CONTAINER_NAME = 'heart-disease-all'

setup-space:
	@mkdir -p .s2i/

train-all:
	@for dir in $(MODEL_DIRS) ; do \
		echo "Building "$$dir ; \
		cd ${PROJECT_ROOT_DIR}$$dir && make build-train && make train ; \
	done

predict-all: create-routes
	@mkdir -p ${PROJECT_ROOT_DIR}/build-context
	@rm -rf ${PROJECT_ROOT_DIR}/build-context/
	mkdir -p ${PROJECT_ROOT_DIR}/build-context/${projectname}
	rsync -av --exclude=/data --exclude=/build-context --exclude=/models --exclude=all ${PROJECT_ROOT_DIR} ${PROJECT_ROOT_DIR}/build-context/${projectname}
	cp -r .s2i requirements.txt ${PROJECT_ROOT_DIR}/build-context
	cp -r ${PROJECT_ROOT_DIR}/../utils ${PROJECT_ROOT_DIR}/build-context
	rsync -av --include="*.py" --exclude="*" . ${PROJECT_ROOT_DIR}/build-context/${projectname}
	rsync -avr --include="setup.sh" --exclude="*" ${PROJECT_ROOT_DIR}/**/ ${PROJECT_ROOT_DIR}/build-context

	s2i build -c ${PROJECT_ROOT_DIR}/build-context c12e/cortex-s2i-daemon-python36-slim:1.0.0 ${CONTAINER_NAME}
	# remove build artifacts
	rm -rf ${PROJECT_ROOT_DIR}/build-context
	docker run --rm  -v $(PROJECT_ROOT_DIR)/models:/action/models -p 5111:5000 -it ${CONTAINER_NAME}

create-routes: setup-space
	echo  "ROUTES=" | tr -d "\n" > .s2i/env
	@for dir in $(MODEL_DIRS) ; do \
		cd ${PROJECT_ROOT_DIR}$$dir && cat .s2i/environment | grep -o -E 'ROUTES=[^ ]+' | sed -e 's/ROUTES=//' | sed -e 's/$$/,/' | tr -d '\n' >> ${CURRENT_DIR}/.s2i/env  ; \
	done
	(cat .s2i/env | sed 's/.$$//') | tee .s2i/environment
	rm -f .s2i/env

test-all:
	@for dir in $(MODEL_DIRS) ; do \
		echo "testing ${CONTAINER_NAME} -"$$dir ; \
		cd ${PROJECT_ROOT_DIR}$$dir && make test-endpoint ; \
	done

predict-all-local: help-local create-routes
	cd ../ && PYTHONPATH=.. python ${PROJECT_ROOT_DIR}/../utils/local_server.py $(shell cat .s2i/environment | grep -o -E 'ROUTES=[^ ]+' | sed -e 's/ROUTES=//')

train-all-local: help-local
	@for dir in $(MODEL_DIRS) ; do \
		echo "training "$$dir locally; \
		cd ${PROJECT_ROOT_DIR}$$dir && make train-local ; \
	done

help-local:
	@echo "make sure all dependencies are installed locally."
	@echo "all deps can be found at certifai-reference-models/all/requirements_local.txt"
	@echo "to install deps from file requirements_local.txt run "
	@echo "pip install -r requirements_local.txt"
