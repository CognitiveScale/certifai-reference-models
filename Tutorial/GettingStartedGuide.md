# Getting Started Guide  
  
This guide explains how to package up your trained model as a web service with a predict API that can be scanned using Certifai
  
  
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

   > refer to function `predict_titanic_survivor` in `titanic_survivor_prediction/predict.py`
  
##  api
  
Exposing model predict as an api using [s2i](https://github.com/openshift/source-to-image) requires  
  
1. creating a `.s2i/environment` config file in the top-level directory with  
   * `ROUTES=<routeName:predictModuleName:predictFunctionName>`  

  > e.g. `ROUTES=titanic_survivor_rf/predict:predict:predict_titanic_survivor` 

2 . creating a `requirements.txt` to install python-dependencies required to run the model inside the container


## build-container 

This command builds the container and packages the code for the model predict web api  

1. s2i build . builderImageName containerName 
   * builderImage (public): `cortex-s2i-daemon-python36-slim:1.0.0`  
 * containerName: name to identify container by 
  
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
  
> *internalPort* will be 5000 in our case   
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