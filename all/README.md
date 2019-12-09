## Training and Predicting all Projects/UseCases together

### To Train all models together

> make sure each model inside project/usecase works with their corresponding `make train` and generates model_binary (.pkl) in the models directory.

1. `make train-projects-all`

    will train all models for all projects and dump the respective model binaries in the models dir


## To start the predict server for all models together

> make sure model binaries(.pkl's) are present in models dir and each model inside project/usecase has the corresponding .s2i/environment file with correct ROUTES defined

1. `make predict-projects-all` 
    
    will load model binaries in memory for all models and all projects/usecases and start a single model server with the correponding routes defined in .s2i/environment in each model
    

    ## To test all the endpoints created using make predict-projects-all 

    > make sure model server is running and httpie is installed locally. 
    
    > To setup httpie visit
      [Httpie](https://httpie.org/)


1.  `make test-all-endpoints`

    will run test against the model server with corresponding inputs defined in `test/test_instances.json` dir inside each model





