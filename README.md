# Cortex Certifai Reference Models

This Repo contains code to train Reference Machine Learning Models for Cortex Certifai and create routes to expose the corresponding predict functionality using web services

All models are trained, exposed (as web-service) and containerized using source-to-image [s2i](https://github.com/openshift/source-to-image)

Instructions to build, train and predict are included inside each project/use-case. Also, all projects can be built together using directions provided in `all` directory

Furthermore, `docs` includes more documentation for code organization and detailed instructions for adding your own projects,models etc. 
