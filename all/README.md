## Training all Projects/UseCases Simultaneously

### Train all use case models

Before you proceed, ensure the models for each project/use case generates the model_binary (.pkl) in the models directory when you run `make train`.

To train all models for all projects simultaneously run:

`make train-projects-all`

The output is stored in the respective model binaries in the models dir.


### Start the predict server for all use case models

Before you proceed, ensure that model binaries(.pkl's) are present in models dir, and each model inside project/use case has the corresponding .s2i/environment file with correct ROUTES defined.

To load model binaries in memory for all project/use case models and start a single model server with the corresponding routes defined in .s2i/environment for each model run:

`make predict-projects-all`

The output is the creation of an endpoint for each model that can be used in Certifai to point to the model.


### Test the endpoints

Before you proceed, ensure that the model server is running and httpie is installed locally.

**NOTE**: To setup httpie visit [Httpie](https://httpie.org/)

To test the model server with corresponding inputs defined in `test/test_instances.json` dir inside each model run:

`make test-all-endpoints`

<The output is . . .>
