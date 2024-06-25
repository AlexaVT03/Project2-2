To view a model's code and how it functions, please open the appropriate model's .ipynb file. 
There, a notebook will show all the previously executed code, including plots, results, print statements and terminal outputs.

In case the model does not show up properly, run the notebook as follows:
1. Select an appropriate python runtime.
2. Replace the absolute file path at the top of the relevant notebook with your own absolute file path. Make sure to replace all '\' with '/'.
3. Run the full notebook. Note that this will take some time, with some models taking longer than others. Please be patient and do not interrupt the runtime.

There is a pre processing script under "NL_DATA" which you NEED to run before using any notebooks. Please find the instructions to this script in "NL_DATA/README.txt"

To run the GUI, simply run the Main.java file.

We are only predicting dates from 05/05/2024 up to and including 07/05/2024. Other dates will not work. 

Predictions for LSTM can be shown without any changes to the code, but for SARIMAX this works different as it predicts on the spot. To make this work, you can follow the steps below.
1. Unzip the 6 zip files found in the models folder in the SARIMAX folder which contain the models for two locations for each zip.
1. Change the model_path in arima.py found in the SARIMAX folder to your path for the models folder found in SARIMAX.
2. Unzip the grib_data_forecast.zip found in the forecast_set folder which is in the NL_data folder. 
2. Change the path to the forecast.csv received from step 2. 

Thank you for reading.

-Group 12-
