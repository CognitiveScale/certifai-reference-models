# Getting Started Guide  
  
This guide explains how to package up your trained model as a web service(inside a docker container) with a predict API that can be scanned using Certifai
  
  
## Table of Contents  
1. [pre-requisites](#pre-requisites)   
2. [predict](#predict)  
3. [api](#api)  
4. [build-container](#build-container)  
5. [run-container](#run-container)  
5. [test-container](#test-container) 
6. [makefile-commands](#makefile)
  
## pre-requisites  
  
1. trained model : can be a model binary (e.g pkl) that can be loaded from disk (during container [build](#build-container) or volume mounted into the container), or <br>
trained model object e.g sklearn.svm.SVC <br> 

    for demo purposes we'll train a sample sklearn model (when container runs) and use that trained model object to run predictions on
   > for reference checkout `titanic_survivor_prediction/train.py`

2. Optional [make](https://www.gnu.org/software/make/) : required when executing commands via makefile or user can choose to run (copy/paste) the commands directly in the terminal

3. [source-to-image (s2i)](https://github.com/openshift/source-to-image)  

4. Optional [Httpie](https://httpie.org/) (Required to run `make test-container`, can use `curl` instead)   

  
## predict     
 Create a predict function that takes a message object as function parameter containing data instances to predict against   
and return list of predictions. 

> for reference checkout `predict_titanic_survivor` in `Tutorial/titanic_survivor_prediction/predict.py`  
  

##  api
  
Exposing model predict as an api using [s2i](https://github.com/openshift/source-to-image) requires  
  
1. creating a `.s2i/environment` config file in the top-level directory with
   * `ROUTES=<routeName:predictModuleName:predictFunctionName>`  
   
     e.g. `ROUTES=titanic_survivor_rf/predict:predict:predict_titanic_survivor`
     
        > for reference checkout `Tutorial/titanic_survivor_prediction/.s2i/environment`
 
> note: for predict api request/response schema refer for docs/instructions.md #Model Predict: Request/Response

  
  
2 . creating a `requirements.txt` to install python-dependencies required to run the model inside the container


## build-container 

This command builds the container and packages the code for the model predict web api.

>note: user needs to be in `Tutorial/titanic_survivor_prediction` directory to run the following command

1. s2i build . builderImageName containerName 
   * builderImageName (publicly available docker image used as base image to build from. Here we will be using `c12e/cortex-s2i-daemon-python36-slim:1.0.0`  
   * containerName: name of the built container
   * . (dot operator) ensures all files/folders in the current dir are added to the container
  
e.g. 
`s2i build . c12e/cortex-s2i-daemon-python36-slim:1.0.0 titanic_survivor_prediction`  
 
```
s2i build . c12e/cortex-s2i-daemon-python36-slim:1.0.0 titanic_survivor_prediction
---> Installing application source...
---> setup.sh not found. Proceeding without ...
---> Installing dependencies ...
...
Build completed successfully
``` 
 
## run-container  

1. runs the container build in [build-container](##build-container)  
  
   * docker run --publish hostPort:containerPort --interactive --tty containerName  
  
> *containerPort* is defined inside the builderImage (5000) and is fixed <br> 
> *hostPort is left for user to specify*
>
 e.g. `docker run --publish 5111:5000 --interactive --tty titanic_survivor_prediction`  
  
```
starting daemon
[2020-03-05 18:51:54 +0000] [1] [INFO] Starting gunicorn 20.0.4
[2020-03-05 18:51:54 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2020-03-05 18:51:54 +0000] [1] [INFO] Using worker: sync
[2020-03-05 18:51:54 +0000] [8] [INFO] Booting worker with pid: 8
2020-03-05 18:51:56,341 - INFO - daemon/daemon: Adding route: /titanic_survivor_rf/predict using function predict:predict_titanic_survivor
```  
  
## test-container
  
using `curl`  
  
```  
curl -X POST \
  http://127.0.0.1:5111/titanic_survivor_rf/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "payload": { "instances": [[3.0,0.0,26.0,0.0,0.0,7.925,2.0],[1.0,0.0,35.0,1.0,0.0,53.1,2.0]]}
}'
```  

`{"payload":{"predictions":[1,1]}}`

using `httpie`  
  
`http -v -j POST :5111/titanic_survivor_rf/predict < test_instances_generated.json`

```
http -v -j POST :5111/titanic_survivor_rf/predict < test_instances_generated.json
POST /titanic_survivor_rf/predict HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 415
Content-Type: application/json
Host: localhost:5111
User-Agent: HTTPie/1.0.3

{
    "payload": {
        "instances": [
            [
                3.0,
                0.0,
                26.0,
                0.0,
                0.0,
                7.925,
                2.0
            ],
            [
                1.0,
                0.0,
                35.0,
                1.0,
                0.0,
                53.1,
                2.0
            ]
        ]
    }
}

HTTP/1.1 200 OK
Connection: close
Content-Length: 34
Content-Type: application/json
Date: Thu, 05 Mar 2020 19:14:55 GMT
Server: gunicorn/20.0.4

{
    "payload": {
        "predictions": [
            1,
            1
        ]
    }
}


```


# makefile

User can directly run `make` commands to build, run and test the container (requires [make](https://www.gnu.org/software/make/) see [pre-requisites](#pre-requisites))

>note: user needs to be in `Tutorial/titanic_survivor_prediction` directory to run the below make commands


1. `make build-container`: [builds](#build-container) the container
2. `make run-container`:  [starts](#run-container) the container
3. `make test-container` : runs a [sample prediction](#test-container) against the container

