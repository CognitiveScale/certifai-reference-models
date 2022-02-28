# Cortex Certifai Reference Models

To create package and start server run

`sh install.sh`

Package is created under `build-package/dist/cortex-certifai-reference-model-server-x.x.x.zip`

Once installed; to start server manually type `startCertifaiModelServer` on the terminal

To test, run `make test`

---

Individual models can be run in a prediction service for debugging using `make predict-local`
from the model folder and `make test-endpoint`.

---

The reference model server currently pins `scikit-learn==0.24.2` to support python 3.6. To
update beyond this (e.g., to v1.0.2) will require python 3.7+. An explicit version should 
still be pinned to avoid warnings when importing the pickles.
