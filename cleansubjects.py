import os

#-----------------------------------------------------------------
#removes all session 2s and left waist sessions from subjects dir
#should only be run once
#------------------------------------------------------------------

# Set the path to the folder you want to clean
FOLDER = "subjects"


def remove_rename_csvs():
    # We are only looking at csv files where the measurements were done in the Right-Pocket,
    # and only the first session
    for filename in os.listdir(FOLDER):
        # Check for 's2' or 'lw' in the filename to remove
        file_path = os.path.join(FOLDER, filename)
        if "s2" in filename.lower() or "lw" in filename.lower():
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
        else:
            # clean file name (all files for some reason have leading whitespace and some have an extra .csv ext)
            new_name = filename.strip().replace('.csv.csv', '.csv')
            os.rename(file_path, os.path.join(FOLDER, new_name))


# Make sure the folder exists
if os.path.exists(FOLDER):
    remove_rename_csvs()

else:
    print(f"Folder '{FOLDER}' does not exist.")
