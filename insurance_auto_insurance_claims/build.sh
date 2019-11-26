#!/bin/bash
set -e

# get target-image-name and model-dir
target=$1
modeldir=$2
jobtype=$3

echo "building model " ${modeldir}

if [[ -z $target || -z $modeldir || -z $jobtype ]]; then
    echo ERROR: Missing argument to "./build.sh <target> <modeldir> <job-type(train/predict)>" 1>&2
    exit 1
fi

# setting build-context init
mkdir -p build-context
rm -rf build-context/*
mkdir build-context/models
mkdir build-context/data
cp -r common_utils build-context/
cp -a ${modeldir}/. build-context/

echo "setting container as ${target} and model-dir as ${modeldir}"

if [ $jobtype == "train" ]; then
    echo "starting train job"       
    cat ${modeldir}/requirements_train.txt > build-context/requirements.txt
    rm build-context/requirements_train.txt build-context/requirements_predict.txt
    # s2i builds
    s2i build -c build-context c12e/cortex-s2i-model-python36-slim:1.0-SNAPSHOT ${target}

elif [ $jobtype == "predict" ]; then
    echo "starting predict job"
    cat ${modeldir}/requirements_predict.txt > build-context/requirements.txt
    rm build-context/requirements_train.txt build-context/requirements_predict.txt
    s2i build -c build-context c12e/cortex-s2i-daemon-python36-slim:1.0-SNAPSHOT ${target}

else
    echo ERROR: Invalid job-type argument to "./build.sh <target> <modeldir> <job-type(train/predict)>" 1>&2

fi

# remove build artifacts
rm -rf build-context