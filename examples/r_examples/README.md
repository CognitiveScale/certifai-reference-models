To install the necessary packages (only needed the first time), run

```install.packages('plumber')```

To set up the api, run (e.g.):

```
library(plumber)
pr <- plumber::plumb("logistic_regression_api.R")
pr$run(port=8551)
```

## Predict

curl -X POST \
 http://localhost:8551/predict \
 -H 'Content-Type: application/json' \
 -d '{"payload": { "instances": [[5,1,1,1,2,1,3,1,1], [4,1,1,3,2,1,3,1,1], [2,1,2,1,2,1,3,1,1]] } }'

