#!/bin/bash

CFI_CURRENT_VERSION_LONG=$(git describe --long --always --match='v*.*' | sed 's/v//')
CFI_CURRENT_VERSION=$(echo ${CFI_CURRENT_VERSION_LONG} | cut -d '-' -f 1)
CFI_VERSION_BUILD_NUM=$(echo ${CFI_CURRENT_VERSION_LONG} | cut -d '-' -f 2-)
CFI_PKG_VERSION=$(echo ${CFI_CURRENT_VERSION} | awk -F. -v OFS=. -v f=3 '{ $$f++ } 1')
CFI_PKG_PREFIX=dist/cortex-certifai-reference-model-server
CFI_PKG_NAME=${CFI_PKG_PREFIX}-${CFI_PKG_VERSION}-${CFI_VERSION_BUILD_NUM}.zip

echo ${CFI_PKG_VERSION}-${CFI_VERSION_BUILD_NUM} > buildReportManifest.txt
cat setup.py | sed "s/__version__ = '.*'/__version__ = '${CFI_PKG_VERSION}'/" > setup.py.tmp
mv setup.py.tmp setup.py

## create package to register package namespace
#python setup.py sdist  --format=zip
#
#mv ${CFI_PKG_PREFIX}-${CFI_PKG_VERSION}.zip ${CFI_PKG_NAME}
#
#pip install ${CFI_PKG_NAME}

# copy models from projects and build-again

# cd ../ && mkdir -p models/ && rm -rf models/* && find . -type f -name '*.pkl' -exec mv {} models/ \;

python setup.py sdist  --format=zip && \
  mv ${CFI_PKG_PREFIX}-${CFI_PKG_VERSION}.zip ${CFI_PKG_NAME} && \
  pip install ${CFI_PKG_NAME}

mkdir -p ../artifacts/packages && rm -rf ../artifacts/packages/*  && \
  cp ${CFI_PKG_NAME} ../artifacts/packages && \
  cp buildReportManifest.txt ../artifacts/
