import os
import pandas as pd
import cfgrib
import xarray

def process_data(dir : str) -> None:
    yearly_df = [] # stores yearly_df for concat later
    
    for file in os.listdir(dir): # looks for grib data in specified path
        if file.endswith('.grib'): # proceeds only if grib (should avoid annoying hidden files)
            filter_by_keys = {'edition': 1}  # select grib file w/ edition 1 (otherwise will not work)

            # open grib file to convert to dataframe
            with cfgrib.open_dataset(file, filter_by_keys = filter_by_keys) as ds:
                pass

            # process data       
            vars_list = list(ds.variables) # xarray format
            selected_vars = [i for i in vars_list if i not in ['number', 'step', 'valid_time']] # exclude some useless variables
            vars = ds[selected_vars] # get dataframe with only specified columns

            # high level cleaning
            df = vars.to_dataframe() # -> pandas
            df = df.reset_index() # removes multi index
            df = df.dropna() # if any NaNs -> drop

            # create dummies for month and hour (will help models maybe)
            df['time'] = pd.to_datetime(df['time']) # sets time to datetime if needed
            df['month'] = df['time'].dt.month # new column with only month
            df['hour'] = df['time'].dt.hour # new column with only hour
            df = pd.get_dummies(df, columns = ['month']) # make dummies for month
            df = pd.get_dummies(df, columns = ['hour']) # make dummies for hour

            # finalize processing
            df = df.set_index('time') # sets index to time column
            yearly_df.append(df) # append df to yearly df list

            # DEBUG
            print("processed 1 year")

    # out of for loop, concat all datasets
    final_df = pd.concat(yearly_df) # concats df
    save_path = os.path.join(dir, 'processed_data.csv')
    final_df.to_csv(save_path)

process_data('path_where_you_want_to_save_the_data')