.PHONY: build-container run-container test-container
SHELL := /bin/bash

build-container:
	s2i build . c12e/cortex-s2i-daemon-python36-slim:1.0.0 titanic_survivor_prediction

run-container:
	docker run --publish 5111:5000 --interactive --tty titanic_survivor_prediction

test-container:
	http -v -j POST :5111/titanic_survivor_rf/predict < test_instances_generated.json
