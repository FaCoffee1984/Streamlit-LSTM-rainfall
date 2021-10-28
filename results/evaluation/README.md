**Structure of the pickle file in this folder**

For each location, the structure is the following:

```
pickled dictionary
       |----------- location
                       |------ predictions (numpy 2D array, values in mm)
                       |------ validation (numpy 2D array, values in mm)
                       |------ difference (numpy 2D array, =predictions-validation, values in mm)
                       |------ rmse (float)
                       |------ training data (pandas df beginning with the cutoff date and ending with the exclusion of the last 24 n_future values)
                       |------ validation (pandas df containing the last 24 n_future values)
 ```                       
