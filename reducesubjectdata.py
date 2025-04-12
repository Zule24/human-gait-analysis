import os
import pandas as pd
from multiprocessing import Pool

#-----------------------------------------------------------------
#removes all irrelevant columns in CSV files to reduce on file size
#------------------------------------------------------------------

# Set the path to the folder you want to clean
FOLDER = "subjects"
# For all dataframes, we only keep these columns:
RELEVANT_COLS = ["loggingTime.txt.",
                 "locationLatitude.WGS84.",
                 "locationLongitude.WGS84.",
                 "locationAltitude.m.",
                 "locationSpeed.m.s.",
                 "motionUserAccelerationX.G.",
                 "motionUserAccelerationY.G.",
                 "motionUserAccelerationZ.G."]

def reduce_cols_in_file(filename):
    file_path = os.path.join(FOLDER, filename)
    pd.read_csv(file_path)[RELEVANT_COLS].to_csv(file_path)
    print("reduced columns for " + filename)

# Make sure the folder exists
if os.path.exists(FOLDER):
    files = [f for f in os.listdir(FOLDER) if f.endswith('.csv')]
    
    N_PROCESSES = 4
    with Pool(N_PROCESSES) as pool:
        pool.map(reduce_cols_in_file, files)

else:
    print(f"Folder '{FOLDER}' does not exist.")
