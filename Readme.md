# Market Mix Model 
- Everything created and implemented from the very basics in Python 
- Code is implemented in such a way so that it can be directly applied to any data as a black box.
- Only thing we have to change is the config file for that data, our model takes care of the rest.

### Dependencies
[x] Statsmodel
[x] Pandas
[x] Numpy 
[x] Flask
[x] json
[x] Sklearn

### What inputs it demands?
- hierarchy (the Brand/Manufacturer/Subbrand or anything given in config)
- Name of the hierarchy
- Geographical level (Ex. All India or some zone region)
- Sub Geographical data( if opted for more specs according to config file)

### The Output contains:-
1. Last dated(Month/Year/ whatever specified) data.
2. The impact of the attributes on the Sales or target variable.

### Further inputs required for predicting the target variable
- All the values for numerical data which are subjected to change and we encounter them as our primary variable for prediction.

### The Output contains:-
- Predicted sales or target variable
- Percentage of the change as compared to the last dated value.
- ###### A recommendation based on the coefficients(derived from the fixed and random effects) for all the parameteres provided.
- Recommended Sales or value of target variable.
