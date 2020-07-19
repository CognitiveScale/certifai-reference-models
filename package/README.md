# Cortex Certifai Reference Model Server

This folder contains the materials to build the Certifai reference model server as a 
python package.

TODO: Create appropriate conda env with things needed for train.
Exclude certain models from package.

TODO: Include soft outputs! Will need changes/extensions to the model SDK.

TODO: How to create dockerfiles for the model apps. 

To build the package:
```
make build-package
```

This trains all the models and saves them into the `./certifaiReferenceModelServer/models` folder. 
The server package is created in `package/dist/cortex-certifai-reference-model-server-<version>>.zip`
and is also installed in the current environment.

Once installed, to start the server type `startCertifaiModelServer` on the terminal.

