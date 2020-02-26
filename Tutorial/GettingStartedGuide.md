# Getting Started Guide  
  
Creating a rest api to expose model's predict functionality  
  
  
## Table of Contents  
1. [pre-requisites](#pre-requisites)   
2. [predict](#predict)  
3. [api](#api)  
4. [build-container](#build-container)  
5. [run-container](#run-container)  
5. [test-container](#test-container)  
  
## pre-requisites  
  
1. trained model  
2. [source-to-image (s2i)](https://github.com/openshift/source-to-image)  
3. [Httpie](https://httpie.org/) (Required to run `make test`)   
  
## predict     
 Create a predict function that takes a message object as function parameter containing data instances to predict against   
and return list of predictions   
   
  
##  api
  
Exposing model predict as an api using [s2i](https://github.com/openshift/source-to-image) requires  
  
1. creating a `.s2i/environment` config file in the top-level directory with  
   * `ROUTES=<routeName:predictModuleName:predictFunctionName>`  
  > e.g. `ROUTES=iris_classification_svc/predict:predict:predict_iris_type`  
  
2. creating a `requirements.txt` to install python-dependencies required to run the model  
  
  
## build-container  
1. s2i build . builderImageName containerName  
   * builderImage (public): `cortex-s2i-daemon-python36-slim:1.0.0`  
 * containerName: name to identify container by   
  
e.g. `s2i build . c12e/cortex-s2i-daemon-python36-slim:1.0.0 iris_classification`  
  
## run-container  
  
1. runs the image build in [build-container](##build-container)  
  
   * docker run --publish hostPort:containerPort --interactive --tty containerName  
  
> *internalPort* will be 5000 in our case   
 e.g. `docker run --publish 5111:5000 --interactive --tty iris_classification`  
  
## test-container
  
using `curl`  
  
```  
curl -X POST \  
 http://localhost:5111/iris_classification_svc/predict \ -H 'Content-Type: application/json' \ -d '{"payload": { "instances": [[ 6.5,3.0,5.5,1.8],[6.7,3.3,5.7,2.5]]}  
}'  
```  
  
using `httpie`  
  
`http -v -j POST :5111/iris_classification_svc/predict < test_instances_generated.json`
