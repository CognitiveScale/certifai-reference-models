# Getting Started Guide


## Table of Contents
1. [train](#train)
2. [predict](#predict)
3. [wrapping](#third-example)


### train

 1. create a train function that takes a message (type: dict) as input containing essentials required 
 to start the model training
    * dataset name (to load the training data from e.g. training_data.csv) 
    * model_name (to save model as e.g. adult-income-rf)
    
 
   > this would be the name by which model is saved on disk adult-income-rf.pkl  
   
### predict   
   
 1 . create a predict function that takes message (type: dict) as input containing essentials required
 to start model prediction
    * data instances to make predictions on
    * model to load
  loads the model saved on disk in [train](#train)
  
 
### predict
### serve model



