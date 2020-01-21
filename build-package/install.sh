#!/bin/bash

# create package to register package namespace
python setup.py sdist  --format=zip
pip install dist/cortex-certifai-reference-model-server-0.5.0.zip

# run train with installed package
cd certifaiReferenceModelServer/all && make train-projects-all-local

# mv models from projects and build-again

cd ../ && mkdir -p models/ && rm -rf models/* && find . -type f -name '*.pkl' -exec mv {} models/ \;

cd .. && python setup.py sdist  --format=zip && pip install dist/cortex-certifai-reference-model-server-0.5.0.zip 

# start installed modelServer package binary
startCertifaiModelServer
