# linear_regression_api.R

# Global code; gets executed at plumb() time.
library(jsonlite)
data(longley)
model <- lm(Employed ~ GNP.deflator + GNP + Unemployed + Armed.Forces + Population + Year, data=longley)


#' predict 'Employed' for set of inputs with  linear regression
#' @post /predict
#' @html
#' @response 200 Returns the predictor
calculate_prediction <- function(payload) {
  ## payload should contain "instances", which is a list of either vectors of inputs, 
  ## or JSONs of inputs obtained using toJSON on a dataframe in R
  test_data <- as.data.frame(payload)
  colnames(test_data) <- variable.names(model)[-1]
  
  # predict and return result
  pred <<- predict(model, test_data)
  pred_list <<- list(payload=list(predictions=pred))
  pred_json <<- toJSON(pred_list)
  return(pred_json)
}




