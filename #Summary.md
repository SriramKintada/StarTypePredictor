#Summary
# In no scaling we just run logistic regression on our data frame and claculate validation and r2score using test dataframe
# In standard we standardise the data and run logistic regression on our data frame and claculate validation and r2score using test dataframe
# In minmaxscaller we operate minmaxscaler on the data and run logistic regression on our data frame and claculate validation and r2score using test dataframe
# In hyperparameter we use GridSearchCVto find best hyperparameter which give better result in prediction
# then we create data frame to make comparision in between these methods
# In fitting we use just basic elif condition on validation score and r2 score to identify fitting