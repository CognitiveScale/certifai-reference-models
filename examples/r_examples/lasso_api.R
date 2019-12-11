# lasso_api.R

# Global code; gets executed at plumb() time.
if(!require(glmnet)){
  install.packages("glmnet")
}
library(glmnet)
data(longley)
library(jsonlite)
set.seed(1234)
x <- model.matrix(Employed~., longley)[,-1]
y <- longley$Employed
model <- glmnet(x, y, alpha=1, lambda=1)

#' predict 'Employed' for set of inputs with  lasso
#' @post /predict
#' @html
#' @response 200 Returns the predictor
calculate_prediction <- function(payload) {
  ## payload should contain "instances", which is a list of  vectors of inputs
  test_data <- as.data.frame(payload)
  test_x = data.matrix(test_data)
  
  # predict and return result
  pred <<- predict(model, test_x)
  pred_list <<- list(payload=list(predictions=pred))
  pred_json <<- toJSON(pred_list)
  return(pred_json)
}
