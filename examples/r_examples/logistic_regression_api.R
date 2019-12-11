# logistic_regression_api.R
"pay"
# Global code; gets executed at plumb() time.
if(!require(mlbench)){
  install.packages("mlbench")
}
if(!require(caret)){
  install.packages("caret")
}
library(mlbench)
library(caret)
data(BreastCancer)
set.seed(1234)


trainIndex <- createDataPartition(BreastCancer$Class, p = .8, 
                                  list = FALSE, 
                                  times = 1)

train <- BreastCancer[trainIndex,]
train <- subset(train, select = -c(Id))
train$Class <- ifelse(train$Class == "benign", 1, 0)
indx <- sapply(train, is.factor)
train[indx] <- lapply(train[indx], function(x) as.numeric(as.character(x)))

default.Cl.thickness <- mean(train$Cl.thickness, na.rm=TRUE)
default.Cell.size <- mean(train$Cell.size, na.rm=TRUE)
default.Cell.shape <- mean(train$Cell.shape, na.rm=TRUE)
default.Marg.adhesion <- mean(train$Marg.adhesion, na.rm=TRUE)
default.Epith.c.size <- mean(train$Epith.c.size, na.rm=TRUE)
default.Bare.nuclei <- mean(train$Bare.nuclei, na.rm=TRUE)
default.Bl.cromatin <- mean(train$Bl.cromatin, na.rm=TRUE)
default.Normal.nucleoli <- mean(train$Normal.nucleoli, na.rm=TRUE)
default.Mitoses <- mean(train$Mitoses, na.rm=TRUE)

train$Cl.thickness[is.na(train$Cl.thickness)] = default.Cl.thickness
train$Cell.size[is.na(train$Cell.size)] = default.Cell.size
train$Cell.shape[is.na(train$Cell.shape)] = default.Cell.shape
train$Marg.adhesion[is.na(train$Marg.adhesion)] = default.Marg.adhesion
train$Epith.c.size[is.na(train$Epith.c.size)] = default.Epith.c.size
train$Bare.nuclei[is.na(train$Bare.nuclei)] = default.Bare.nuclei
train$Bl.cromatin[is.na(train$Bl.cromatin)] = default.Bl.cromatin
train$Normal.nucleoli[is.na(train$Normal.nucleoli)] = default.Normal.nucleoli
train$Mitoses[is.na(train$Mitoses)] = default.Mitoses
# Building the model
model <- glm(Class ~.,family=binomial(link='logit'),data=train)


#' predict 'Class' for set of inputs with  logistic regression
#' @post /predict
#' @html
#' @response 200 Returns the predictor
calculate_prediction <- function(payload) {
  ## payload should contain "instances", which is a list of either vectors of inputs, 
  ## or JSONs of inputs obtained using toJSON on a dataframe in R
  test_data <- as.data.frame(payload)
  colnames(test_data) <- c("Cl.thickness","Cell.size","Cell.shape",   
                           "Marg.adhesion","Epith.c.size","Bare.nuclei","Bl.cromatin",    
                           "Normal.nucleoli", "Mitoses")
  
  test_data$Cl.thickness[is.na(test_data$Cl.thickness)] = default.Cl.thickness
  test_data$Cell.size[is.na(test_data$Cell.size)] = default.Cell.size
  test_data$Cell.shape[is.na(test_data$Cell.shape)] = default.Cell.shape
  test_data$Marg.adhesion[is.na(test_data$Marg.adhesion)] = default.Marg.adhesion
  test_data$Epith.c.size[is.na(test_data$Epith.c.size)] = default.Epith.c.size
  test_data$Bare.nuclei[is.na(test_data$Bare.nuclei)] = default.Bare.nuclei
  test_data$Bl.cromatin[is.na(test_data$Bl.cromatin)] = default.Bl.cromatin
  test_data$Normal.nucleoli[is.na(test_data$Normal.nucleoli)] = default.Normal.nucleoli
  test_data$Mitoses[is.na(test_data$Mitoses)] = default.Mitoses
  
  pred <<- ifelse(predict(model, test_data, type = "response")>0.5, 1, 0)
 
  pred_list <<- list(payload=list(predictions=pred))
  pred_json <<- toJSON(pred_list)
  return(pred_json)
}
