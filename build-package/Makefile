.PHONY: build-package build_image clean_build_space test

SHELL := /bin/bash

clean_build_space:
	rm -rf dist/*

build_package: clean_build_space
	echo "building certifai reference model server python package .."
	./install.sh

test:
	cd certifaiReferenceModelServer/all && make test-all-endpoints
