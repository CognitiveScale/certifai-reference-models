# logistic_regression_api.R
"pay"
# Global code; gets executed at plumb() time.

# caret is needed for the train/test split; can remove if we aren't doing that.
if(!require(jsonlite)){
  install.packages("jsonlite")
}
library(jsonlite)
if(!require(caret)){
  install.packages("caret")
}
library(caret)

data <- read.csv(file='../german_credit/data/german_credit-decoded.csv', header=TRUE, sep=',')
set.seed(1234)

## here I'm assuming we're generating a dynamic train/test split. For a static split, 
## read in train_data using read.csv directly, using the format above. 

trainIndex <- createDataPartition(data$outcome, p = .8, 
                                  list = FALSE, 
                                  times = 1)
train_data <- data[trainIndex,]

## to generate test set:
## data <- read.csv(file='../german_credit/data/german_credit-decoded.csv', header=TRUE, sep=',')
## set.seed(1234)
## trainIndex <- createDataPartition(data$outcome, p = .8, 
##                                  list = FALSE, 
##                                  times = 1)
##test_data <- data[-trainIndex,]

num_col <- c(2, 5, 8, 11, 16, 18) # note, R is one-based not zero-based
cat_col <- c(1, 3, 4, 6, 7, 9, 10, 12, 13, 14, 15, 17, 19, 20)

for(cat in cat_col){
  train_data[[cat]] <- factor(train_data[[cat]], levels=levels(data[[cat]]))
  ## the levels command makes sure we include any levels that aren't in the training set
  ## Will need to edit to read in a pre-defined list of levels, if we aren't dynamically 
  ## creating the train/test split
}

defaultValues <- vector(mode="list", length=20)
for (num in num_col){
  train_data[[num]] <- as.numeric(as.character(train_data[[num]])) # will convert any non-numeric to NA, and make sure e.g. "1" gets coded as 1
  defaultValues[[num]] <- mean(train_data[[num]], na.rm=TRUE) # mean imputation for missing values
  train_data[[num]][is.na(train_data[[num]])] = defaultValues[[num]]
  train_data[[num]] = scale(train_data[[num]]) # analogous to the standard scalar used in python
}

train_data$outcome <- train_data$outcome - 1 # originally encoded as 1/2

# Building the model
model <- glm(outcome ~.,family=binomial(link='logit'),data=train_data)


#' predict 'Class' for set of inputs with  logistic regression
#' @post /predict
#' @html
#' @response 200 Returns the predictor
calculate_prediction <- function(payload) {
  ## payload should contain "instances", which is a list of either vectors of inputs, 
  ## or JSONs of inputs obtained using toJSON on a dataframe in R.
  ## This assumes that your inputs inlcude the "output" attribute,  but doesn't
  ## use it for prediction. To change, replace colnames(data) with colnames(data)[-21]
  test_data <- as.data.frame(payload)
  colnames(test_data) <- colnames(data)
  
  for(cat in cat_col){
    test_data[[cat]] <-  factor(test_data[[cat]], levels=levels(data[[cat]]))
    ## Will need to edit to read in a pre-defined list of levels, if we aren't dynamically 
    ## creating the train/test split
  }
  
  for (num in num_col){
    test_data[[num]] <- as.numeric(as.character(test_data[[num]]))
    test_data[[num]][is.na(test_data[[num]])] = defaultValues[[num]]
    test_data[[num]] <- scale(test_data[[num]], 
                              center=attr(train_data[[num]], "scaled:center"),
                              scale=attr(train_data[[num]], "scaled:scale")
                              ) # scales using same values as training data
  }
  
  pred <<- ifelse(predict(model, test_data, type = "response")>0.5, 2, 1)
  # note, using original 1/2 rather than 0/1 -- edit end of previous line if you want 0,1
 
  pred_list <<- list(payload=list(predictions=pred))
  pred_json <<- toJSON(pred_list)
  return(pred_json)
}
