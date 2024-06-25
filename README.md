# Welcome to our project 2-2 submission. 

# In the "Python" directory, you can find all the notebooks and scripts we used to:
1) fetch the data from the CDSAPI
2) pre-process the data
3) train our models

## In the LSTM/models and SARIMA/models, you will find the models we trained. If you want to use them in our notebooks, please unzip them in the "models" directory of each model. 

###  If you want to check the code behind any of those topics, please find them in the "Python" directory.

# In the "NL_data" directory, you can find all the files we used for this project. You need to follow the following steps to get the files in .csv format:
1) locate the "data_set_1" and "data_set_2" directories
2) unzip the archives you find in these directories, and DO NOT rename any file, DO NOT move any file to another location
3) run the "data_preprocessor.py" script, and CHANGE THE "path1" and "path2" variables in this script to the "data_set_1" and "data_set_2" paths
4) let the script run, it takes a while (20 minutes)

# CHECKING OUR FORECASTS USING OUR GUI
### For our two most "interesting" models, namely the SARIMA and the LSTM, you can check forecasts up to 72 hours in the future using our GUI.
## In the "gui_forecast" directory, you will find the Java files you need to run our GUI. Please run the "GUI.java" file, and experiment with our forecasts.

# IMPORTANT
### You will notice that this repository contains many other Java-related files. These files are supposed to establish a Java-Python connection, and has a GUI implementation which uses Python to make forecasts on the spot. The reason why we are not mentioning it earlier, and the reason for which we do not recommend using this GUI, is that it creates many issues for some computers, and works well on others. Our "gui_forecast" is a GUI which uses only Java, and simply reads from arrays to present its forecasts.

### If you do want to try this GUI, please run the "Main.java" file in src/.. 

Thank you for reading.

-Group 12-
