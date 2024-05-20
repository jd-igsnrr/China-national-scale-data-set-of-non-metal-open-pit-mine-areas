import os

# Define the directory path where the script should look for files
directory_path = './labels'

# Iterate over all files in the specified directory
for filename in os.listdir(directory_path):
    # Construct the full file path
    file_path = os.path.join(directory_path, filename)
    # Check if the file is a .txt file and if it is empty
    if filename.endswith('.txt') and os.path.getsize(file_path) == 0:
        # Delete the file
        os.remove(file_path)