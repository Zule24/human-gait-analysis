import os
import shutil

#------------------------------------------
#THIS DELETES EVERYTHING IN PROCESSED_DATA
#BE CAREFUL
#-------------------------------------------


# Path to the folder to clean
folder = "processed_data"

# Check if the folder exists
if os.path.exists(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            # If it's a file or a symbolic link, remove it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            # If it's a directory, remove it and all its contents
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
else:
    print(f"Folder '{folder}' does not exist.")