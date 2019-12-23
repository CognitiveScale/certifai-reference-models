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
projectname=$(pwd | awk -F / '{print $NF}')
mkdir -p build-context
rm -rf build-context/*
mkdir -p build-context/${projectname}
mkdir build-context/${projectname}/models
mkdir build-context/${projectname}/data

# copy files

# remove trailing /
modeldir=${modeldir%/}
modelname=$(echo ${modeldir} | awk -F / '{print $NF}')
rsync -av --exclude=.s2i  ${modeldir} build-context/${projectname}/
cp -r ../utils build-context/
cp -r common_utils build-context/${projectname}/
cp -r ${modeldir}/.s2i build-context

echo "setting container as ${target} and model-dir as ${modeldir}"

if [ $jobtype == "train" ]; then
    echo "starting train job"       
    cat ${modeldir}/requirements_train.txt > build-context/requirements.txt
    rm build-context/${projectname}/${modelname}/requirements_train.txt build-context/${projectname}/${modelname}/requirements_predict.txt
    # s2i builds
    s2i build -c build-context c12e/cortex-s2i-model-python36-slim:1.0.0 ${target}

elif [ $jobtype == "predict" ]; then
    echo "starting predict job"
    cat ${modeldir}/requirements_predict.txt > build-context/requirements.txt
    rm build-context/${projectname}/${modelname}/requirements_train.txt build-context/${projectname}/${modelname}/requirements_predict.txt
    s2i build -c build-context c12e/cortex-s2i-daemon-python36-slim:1.0.0 ${target}

else
    echo ERROR: Invalid job-type argument to "./build.sh <target> <modeldir> <job-type(train/predict)>" 1>&2

fi

# remove build artifacts
rm -rf build-context