To install the necessary packages (only needed the first time), run

```install.packages('plumber')```

To set up the api, run (e.g.):

```
library(plumber)
pr <- plumber::plumb("linear_regression_api.R")
pr$run(port=8551)
```

## Predict

You can either pass test data as a list of lists, e.g.


```
curl -X POST \
 http://localhost:8551/predict \
 -H 'Content-Type: application/json' \
 -d '{"payload": {"instances": [["MO", 473.8992, "Basic", "College", "Unemployed", "M", 0, "Suburban", "Single", 67, 23, 5, 0, 3, "Personal L3", "Collision", "Agent", 482.4, "Four-Door Car", "Small"], ["NE", 881.9019, "Basic", "High School or Below", "Employed", "M", 99845, "Suburban", "Married", 110, 23, 25, 1, 8, "Corporate L3", "Hail", "Branch", 528, "SUV", "Medsize"], [ "MO", 394.5242, "Basic", "College", "Medical Leave", "M", 28855, "Suburban", "Married", 101, 12, 59, 0, 1, "Personal L2", "Scratch/Dent", "Call Center", 647.442, "SUV", "Medsize"]] } }'
```

or as a list of JSONS. To transform a dataframe `df` into a list of JSONs in `R`, use

```
require(jsonlite)
toJSON(df)
```

you can then query the model using

```
curl -X POST \
 http://localhost:8551/predict \
 -H 'Content-Type: application/json' \
 -d '{"payload": { "instances": [{"State.Code":"MO","Claim.Amount":473.8992,"Coverage":"Basic","Education":"College","EmploymentStatus":"Unemployed","Gender":"M","Income":0,"Location.Code":"Suburban","Marital.Status":"Single","Monthly.Premium.Auto":67,"Months.Since.Last.Claim":23,"Months.Since.Policy.Inception":5,"Number.of.Open.Complaints":0,"Number.of.Policies":3,"Policy":"Personal L3","Claim.Reason":"Collision","Sales.Channel":"Agent","Total.Claim.Amount":482.4,"Vehicle.Class":"Four-Door Car","Vehicle.Size":"Small"},{"State.Code":"NE","Claim.Amount":881.9019,"Coverage":"Basic","Education":"High School or Below","EmploymentStatus":"Employed","Gender":"M","Income":99845,"Location.Code":"Suburban","Marital.Status":"Married","Monthly.Premium.Auto":110,"Months.Since.Last.Claim":23,"Months.Since.Policy.Inception":25,"Number.of.Open.Complaints":1,"Number.of.Policies":8,"Policy":"Corporate L3","Claim.Reason":"Hail","Sales.Channel":"Branch","Total.Claim.Amount":528,"Vehicle.Class":"SUV","Vehicle.Size":"Medsize"},{"State.Code":"MO","Claim.Amount":394.5242,"Coverage":"Basic","Education":"College","EmploymentStatus":"Medical Leave","Gender":"M","Income":28855,"Location.Code":"Suburban","Marital.Status":"Married","Monthly.Premium.Auto":101,"Months.Since.Last.Claim":12,"Months.Since.Policy.Inception":59,"Number.of.Open.Complaints":0,"Number.of.Policies":1,"Policy":"Personal L2","Claim.Reason":"Scratch/Dent","Sales.Channel":"Call Center","Total.Claim.Amount":647.442,"Vehicle.Class":"SUV","Vehicle.Size":"Medsize"}] } }'
```

Note that if you have unescaped newline characters in the JSON passed to the model, then you will get the following warning:

```
Warning in if (stri_startswith_fixed(body, "{")) { :
  the condition has length > 1 and only the first element will be used
```

This should not affect the outcome.