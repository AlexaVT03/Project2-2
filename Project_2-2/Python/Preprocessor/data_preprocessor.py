import os
import pandas as pd
import cfgrib
import xarray as xr

# warning this code isn't amazingly well optimized, you need more than 8gb ram to run it, otherwise it crashes. 16gb is really tight too

final_df = pd.DataFrame()
final_df_2 = pd.DataFrame()
final_df_3 = pd.DataFrame()
final_df_4 = pd.DataFrame()

def process_data(dir : str) -> None:
    yearly_df_1 = [] # stores yearly_df for concat later

    for file in os.listdir(dir): # looks for grib data in specified path
        if file.endswith('.idx'): # this wipes all .idx files, otherwise this is prone to errors
            file_path_ = os.path.join(dir, file)
            os.remove(file_path_)

        elif file.endswith('.grib'): # proceeds only if grib (should avoid annoying hidden files)
            print("found .grib file")
            file_path = os.path.join(dir, file)

            filter_by_keys = {'edition' : 1}  # select grib file w/ edition 1 (otherwise will not work)

            # open 1st edition .grib
            with xr.open_dataset(file_path, backend_kwargs = {'filter_by_keys': filter_by_keys}) as ds:
                # df = ds.to_dataframe()
                pass

            # process data 1st ed
            print("processing .grib file...")
            selected_vars = ['latitude', 'longitude', 'time', 'u10', 'v10', 'd2m', 't2m', 'tcc'] # exclude some useless variables
            vars = ds[selected_vars] # get dataframe with only specified columns

            # high level cleaning
            df_1 = vars.to_dataframe() # -> pandas
            df_1.reset_index(inplace = True)# removes multi index
            df_1.dropna(inplace = True) # if any NaNs -> drop
            df_1.sort_values('time', inplace = True)
            
            # set index, datetime
            df_1.set_index('time', inplace = True)
            df_1.index = pd.DatetimeIndex(df_1.index)

            # create dummies for month and hour (will help models maybe)
            df_1['month'] = df_1.index.month # new column with only month
            df_1 = pd.get_dummies(df_1, columns = ['month']) # make dummies for month

            # finalize processing
            yearly_df_1.append(df_1) # append df to yearly df list
            print("SUCCESFULLY PROCESSED YEAR")

    # out of for loop, concat all datasets
    print("MERGING DATAFRAMES...")
    global final_df
    final_df = pd.concat(yearly_df_1)
    final_df.to_csv(os.path.join(dir, "p1.csv"))
    del yearly_df_1
    del df_1
    print("OPERATION FINISHED WITHOUT ERRORS")

def process_data_2(dir : str) -> None:
    yearly_df_2 = [] # stores yearly_df for concat later

    for file in os.listdir(dir): # looks for grib data in specified path
        if file.endswith('.idx'): # this wipes all .idx files, otherwise this is prone to errors
            file_path_ = os.path.join(dir, file)
            os.remove(file_path_)

        elif file.endswith('.grib'): # proceeds only if grib (should avoid annoying hidden files)
            print("found .grib file")
            file_path = os.path.join(dir, file)

            filter_by_keys_2 = {'edition' : 2} # some variables somehow end up in 2nd edition .grib (it's only precipitation type..)

            # open 2nd edition .grib
            with xr.open_dataset(file_path, backend_kwargs = {'filter_by_keys': filter_by_keys_2}) as ds_2:
                # df_2 = ds_2.to_dataframe()
                pass

            # process data 2nd ed
            print("processing data...")
            selected_vars_2 = ['ptype', 'valid_time'] # precipitation type
            vars_2 = ds_2[selected_vars_2]

            df_2 = vars_2.to_dataframe()
            df_2.reset_index(inplace = True)
            df_2.dropna(inplace = True)
            df_2['time'] = df_2['valid_time']
            df_2.drop(columns = ['valid_time'], axis = 1, inplace = True)
            df_2.sort_values('time', inplace = True)
            df_2 = df_2[['time', 'ptype']]
            
            # set index, datetime
            df_2.set_index('time', inplace = True)
            df_2.index = pd.DatetimeIndex(df_2.index)

            # finalize processing
            yearly_df_2.append(df_2) # append df to yearly df list
            print("SUCCESFULLY PROCESSED YEAR")

    # out of for loop, concat all datasets
    print("MERGING DATAFRAMES...")
    global final_df_2
    final_df_2 = pd.concat(yearly_df_2)
    final_df_2.to_csv(os.path.join(dir, "p2.csv"))
    del yearly_df_2
    del df_2
    print("OPERATION FINISHED WITHOUT ERROR")

def process_data_3(dir : str, csv_name : str) -> None:
    print("finalizing processing...")
    save_path = os.path.join(dir, csv_name)
    df1 = final_df
    df2 = final_df_2
    df3 = pd.concat([df1, df2], axis = 1)
    # df3.drop(columns = ['Unnamed: 0.1', 'number', 'step', 'surface', 'valid_time'], axis = 1, inplace = True)
    df3.to_csv(save_path)
    print("SUCCESFULLY MERGED DATA")
    print(f"FINAL CSV FILE SAVED TO: {save_path}")
    
def process_data_4(dir : str) -> None:
    yearly_df_4 = [] # stores yearly_df for concat later

    for file in os.listdir(dir): # looks for grib data in specified path
        if file.endswith('.idx'): # this wipes all .idx files, otherwise this is prone to errors
            file_path_ = os.path.join(dir, file)
            os.remove(file_path_)

        elif file.endswith('.grib'): # proceeds only if grib (should avoid annoying hidden files)
            file_path = os.path.join(dir, file)

            filter_by_keys_4 = {'edition' : 1}

            # open 2nd edition .grib
            with xr.open_dataset(file_path, backend_kwargs = {'filter_by_keys': filter_by_keys_4}) as ds_4:
                # df_2 = ds_2.to_dataframe()
                pass

            # process data 2nd ed
            selected_vars_4 = ['valid_time', 'e', 'sf', 'pev', 'fdir', 'tp']
            vars_4 = ds_4[selected_vars_4]

            df_4 = vars_4.to_dataframe()
            df_4.reset_index(inplace = True)
            # df_3.dropna(inplace = True)
            df_4 = df_4.fillna(0)
            df_4['time'] = df_4['valid_time']
            df_4.drop(columns = ['valid_time'], axis = 1, inplace = True)
            df_4 = df_4[['time', 'e', 'sf', 'pev', 'fdir', 'tp']]

            # finalize processing
            yearly_df_4.append(df_4) # append df to yearly df list

    # out of for loop, concat all datasets
    save_path = os.path.join(dir, "p3.csv")
    global final_df_4
    final_df_4 = pd.concat(yearly_df_4)
    final_df_4['time'] = final_df_4['time'].astype(str).str.strip()
    final_df_4['time'] = final_df_4['time'].str[:11]
    final_df_4.reset_index(inplace = True)
    final_df_4 = final_df_4[['time', 'e', 'sf', 'pev', 'fdir', 'tp']]
    final_df_4.sort_values('time', inplace = True)
    final_df_4.set_index('time', inplace = True)
    #final_df_4 = final_df_4.iloc[975:]
    #final_df_4 = final_df_4.iloc[:24512085]
    final_df_4.to_csv(save_path)
    # final_df_4.index = pd.RangeIndex(start=0, stop=len(final_df_4), step=1)

    # free some memory
    del yearly_df_4
    del df_4

def process_data_5(dir : str, csv_name : str) -> None:
    print("finalizing processing 2/2...")
    save_path = os.path.join(dir, csv_name)
    df1 = final_df_3
    df2 = final_df_4
    df1.sort_values('time', inplace = True)
    df2.sort_index(inplace = True)
    df1.index = df2.index
    df3 = pd.concat([df1, df2], axis = 1)
    # df3.drop(columns = ['Unnamed: 0.1', 'number', 'step', 'surface', 'valid_time'], axis = 1, inplace = True)
    df3.to_csv(save_path)
    print("SUCCESFULLY MERGED DATA")
    print(f"FINAL CSV FILE SAVED TO: {save_path}")

#process_data('/Users/lpaggen/Documents/DACS COURSES/Project2-2/Project_2-2/NL_data/train_set')
#process_data_2('/Users/lpaggen/Documents/DACS COURSES/Project2-2/Project_2-2/NL_data/train_set')
#process_data_3('/Users/lpaggen/Documents/DACS COURSES/Project2-2/Project_2-2/NL_data/train_set', 'processed_data.csv')
process_data_4('/Users/lpaggen/Documents/DACS COURSES/Project2-2/Project_2-2/NL_data/new_train')
#process_data_5('/Users/lpaggen/Documents/DACS COURSES/Project2-2/Project_2-2/NL_data/train_set', 'final.csv')
