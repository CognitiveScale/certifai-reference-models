# Adding Ml Models to Projects

To add models to available projects:-
1. create a model dir (e.g logisticRegression, catboost etc.)
2. add a training module (e.g train.py) and a predict module (eg. predict.py)
3. to add train and predict dependencies create files named `requirements_train.txt` and `requirements_predict.txt` respectively in the root directory
   > note dependencies are installed using pip
4. additional native dependencies can be installed with a `setup.sh` script present in the root directory
5. train && predict(service routes) are handled using an .s2i/environment file. To create such config add a `.s2i/environment` file at the root dir.
6. structure of `.s2i/environment` file

```
ROUTES=serviceroute:predictModule:predictFunction
TRAIN_MODULE=<module containing train.py>
TRAIN_FUNCTION=<function to invoke to start model training>
```

7. to build the training container: 
> `s2i build -c . c12e/cortex-s2i-model-python36-slim:1.0-SNAPSHOT <TRAIN_CONTAINER_NAME>`

8. to run the training container:
>  `docker run --rm  -v $(PROJECT_ROOT_DIR)/data:/model/data -v $(PROJECT_ROOT_DIR)/models:/model/models -e TRAIN=1 -e PAYLOAD=${PAYLOAD} -it --rm ${TRAIN_CONTAINER_NAME}`

9. to build the predict container: 
> `s2i build -c . c12e/cortex-s2i-daemon-python36-slim:1.0-SNAPSHOT ${PREDICT_CONTAINER_NAME}`

10. to run the predict container:
> `docker run --rm  -v $(PROJECT_ROOT_DIR)/models:/action/models -e MODElNAME=${MODEL_NAME} -p 5111:5000 -it ${CONTAINER_NAME}-predict`
