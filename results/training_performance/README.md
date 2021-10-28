**Structure of the pickle file in this folder**

For each location, the structure is the following:

```
training_perf.pkl
         |----------- location
                         |------ accuracy during training (list of floating point values)
                         |------ losses during training (list of floating point values)
                         |------ validation (numpy 2D array, values in mm)
                         |------ sc (fit standard scaler, one for each location)
                         |------ result_timestamp (time index beginning with the cutoff date but without the last 24 n_future values)
                         |------ result_timestamp (time index with the last 24 n_future values)
 ```        

 To load this pickle, use:
 ```python
    with open(filepath, 'rb') as f: #'rb' stands for "read binary"
        x = pickle.load(f)
 ```
