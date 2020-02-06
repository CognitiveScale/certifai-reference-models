#!/bin/bash

CFI_CURRENT_VERSION_LONG=$(git describe --long --always --match='v*.*' | sed 's/v//')
CFI_CURRENT_VERSION=$(echo ${CFI_CURRENT_VERSION_LONG} | cut -d '-' -f 1)
CFI_VERSION_BUILD_NUM=$(echo ${CFI_CURRENT_VERSION_LONG} | cut -d '-' -f 2-)
CFI_PKG_VERSION=$(echo ${CFI_CURRENT_VERSION} | awk -F. -v OFS=. -v f=3 '{ $$f++ } 1')

echo ${CFI_PKG_VERSION}-${CFI_VERSION_BUILD_NUM} > buildReportManifest.txt
sed -i '' "s/__version__ = '.*'/__version__ = '${CFI_PKG_VERSION}'/" setup.py

# create package to register package namespace
python setup.py sdist  --format=zip

mv dist/cortex-certifai-reference-model-server-${CFI_PKG_VERSION}.zip dist/cortex-certifai-reference-model-server-${CFI_PKG_VERSION}-${CFI_VERSION_BUILD_NUM}.zip

pip install dist/cortex-certifai-reference-model-server-${CFI_PKG_VERSION}-${CFI_VERSION_BUILD_NUM}.zip

run train with installed package
cd certifaiReferenceModelServer/all && make train-projects-all-local

# mv models from projects and build-again

cd ../ && mkdir -p models/ && rm -rf models/* && find . -type f -name '*.pkl' -exec mv {} models/ \;

cd .. && python setup.py sdist  --format=zip && mv dist/cortex-certifai-reference-model-server-${CFI_PKG_VERSION}.zip dist/cortex-certifai-reference-model-server-${CFI_PKG_VERSION}-${CFI_VERSION_BUILD_NUM}.zip && pip install dist/cortex-certifai-reference-model-server-${CFI_PKG_VERSION}-${CFI_VERSION_BUILD_NUM}.zip