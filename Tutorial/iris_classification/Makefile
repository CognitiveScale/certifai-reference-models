.PHONY: build-container run-container test-container
SHELL := /bin/bash

build-container:
	s2i build . c12e/cortex-s2i-daemon-python36-slim:1.0.0 iris_classification

run-container:
	docker run --publish 5111:5000 --interactive --tty iris_classification

test-container:
	http -v -j POST :5111/iris_classification_svc/predict < test_instances_generated.json
