import os
import re

def remove_brackets_from_filenames(root_directory):
    # Iterate through all files in the directory tree starting from root_directory
    for root, dirs, files in os.walk(root_directory):
        for filename in files:
            # Remove text within parentheses (using Chinese brackets) using regex
            new_filename = re.sub(r'\（.*?\）', '', filename)
            if new_filename != filename:
                # Rename the file to the new filename without the bracketed text
                os.rename(os.path.join(root, filename), os.path.join(root, new_filename))

# Replace 'your_directory_path' with the path to your root directory
remove_brackets_from_filenames('.')