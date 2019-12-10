# Cortex Certifai Reference Models

This repo contains code to train reference machine learning models for Cortex Certifai and create routes to expose the corresponding predict functionality using web services.

All models are trained, exposed (as web-service), and containerized using source-to-image [s2i](https://github.com/openshift/source-to-image).

Instructions to build, train, and predict are included inside each project/use-case. Also, all projects can be built together using instructions provided in `all` directory.

In addition, the `docs` folder includes to assist with code organization and detailed instructions for adding your own projects, models, datasets, and evaluations.
