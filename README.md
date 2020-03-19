# Cortex Certifai Reference Models

This repo contains code to train reference machine learning models for Cortex Certifai and create routes to expose the corresponding predict functionality using web services.

All models are trained, exposed (as web-service), and containerized using source-to-image [s2i](https://github.com/openshift/source-to-image).

Please refer to `Tutorial/GettingStartedGuide.md` for a gentle introduction to using `s2i` for packaging a single model to be executed inside a 
docker container and accessible via a predict API.

For more complex, reference use-cases with multiple models, shared utilities please refer to specific examples like bank_marketing, finance_income_prediction etc.

Where instructions to build, train, and predict are included inside each project/use-case. Also, all projects can be built together using instructions provided in `all` directory.

In addition, the `docs` folder includes to assist with code organization and detailed instructions for adding your own projects, models, datasets, and evaluations.

