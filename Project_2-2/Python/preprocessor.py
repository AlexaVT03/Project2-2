import os
import pandas as pd

directory = 'YOUR PATH/Project_2-2/Data/'  # CHANGE TO OWN PATH

daily_df_list = [] # keeps daily df

monthly_df_list = [] # keeps all monthly df

yearly_df_list = []  # this keeps all yearly DF

country_of_interest = 'NL'  # will add some country codes, NL, GM, etc work

# iterates over year, month -> not clean but works exactly as intended
for year_dir in os.listdir(directory):  # looks in year dir
    if year_dir != ".DS_Store":  # ignore mac files
        yearly_df_list.clear()  # reset monthly_df_list for each year
        year_dir_path = os.path.join(directory, year_dir)  # dir updated

        monthly_df_list = []  # reset monthly_df_list for each year

        for month_dir in os.listdir(year_dir_path):  # looks in month dir
            if month_dir != ".DS_Store":  # ignore mac files
                month_dir_path = os.path.join(year_dir_path, month_dir)

                daily_df_list = []  # reset daily_df_list for each month

                for day_file in os.listdir(month_dir_path):  # in dir with daily observations
                    day_file_path = os.path.join(month_dir_path, day_file)  # get the path to the daily observations

                    # check if csv (otherwise txt)
                    if day_file_path.endswith('.csv'):

                        # get the date part of the file
                        parts = day_file.split('_')
                        date_part = parts[3]

                        # rename file to only date
                        new_filename = os.path.join(month_dir_path, f"{date_part}.csv")
                        os.rename(day_file_path, new_filename)

                        # make a df for the current daily observation csv -> will concat them later
                        daily_df = pd.read_csv(new_filename)  # this makes a pandas df for the daily csv

                        # extract only selected country for the df
                        daily_df = daily_df[daily_df['primary_station_id'].str[:2] == country_of_interest]

                        # append the df to a list
                        daily_df_list.append(daily_df)  # append the daily df to a list

                    # delete if text file
                    elif day_file.endswith('.txt'):
                        # Remove the text file
                        os.remove(os.path.join(month_dir_path, day_file))

                # concat daily DF -> monthly DF
                monthly_df = pd.concat(daily_df_list)
                monthly_df_list.append(monthly_df)

        # DEBUG
        print(len(monthly_df_list))

        # concat monthly DF -> yearly DF
        yearly_df = pd.concat(monthly_df_list)

        # save yearly DF
        yearly_filename = os.path.join(year_dir_path, f"{year_dir}_yearly.csv")
        yearly_df.to_csv(yearly_filename, index=False)
