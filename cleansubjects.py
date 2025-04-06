import os

#-----------------------------------------------------------------
#removes all session 2s and left waist sessions from subjects dir
#should only be run once
#------------------------------------------------------------------

# Set the path to the folder you want to clean
folder = "subjects"

# Make sure the folder exists
if os.path.exists(folder):
    for filename in os.listdir(folder):
        # Check for 's2' or 'lw' in the filename
        if "s2" in filename.lower() or "lw" in filename.lower():
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
else:
    print(f"Folder '{folder}' does not exist.")
