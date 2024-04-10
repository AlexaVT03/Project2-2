import os

directory = '***YOUR PATH***/Project_2-2/Data/' # CHANGE TO OWN PATH

# iterates over year, month -> not clean but works exactly as intended
for year_dir in os.listdir(directory): # looks in year dir
    if year_dir != ".DS_Store": # ignore mac files
        directory = '***YOUR PATH***/Project_2-2/Data/' # reset path for each iter (change later/make modular..)
        year_dir_path = os.path.join(directory, year_dir) # dir updated

        for month_dir in os.listdir(year_dir_path): # looks in month dir
            if month_dir != ".DS_Store": # ignore mac files
                month_dir_path = os.path.join(year_dir_path, month_dir)

                for day_file in os.listdir(month_dir_path):
                    day_file_path = os.path.join(month_dir_path, day_file)
                    
                    # check if csv (otherwise txt)
                    if day_file_path.endswith('.csv'):
                        
                        # get the date part of the file
                        parts = day_file_path.split('_')
                        date_part = parts[4] # don't understand why 4 and not 3 ? 
                        
                        # rename file to only date
                        new_filename = os.path.join(month_dir_path, f"{date_part}.csv")
                        os.rename(day_file_path, new_filename)
                        
                    # delete if text file
                    elif day_file.endswith('.txt'):
                        # Remove the text file
                        os.remove(os.path.join(month_dir_path, day_file))
