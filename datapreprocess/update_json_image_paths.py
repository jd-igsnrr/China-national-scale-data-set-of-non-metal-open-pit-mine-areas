import os
import json

def update_imagepath(json_dir):
    # Iterate over all files in the json_dir directory
    for file_name in os.listdir(json_dir):
        # Check if the current file is a JSON file
        if file_name.endswith('.json'):
            # Construct the full file path
            json_path = os.path.join(json_dir, file_name)
            # Open the JSON file for reading
            with open(json_path, 'r') as json_file:
                data = json.load(json_file)
            # Update the 'imagePath' field with the new image file name
            data['imagePath'] = "..\\image\\" + os.path.splitext(file_name)[0] + '.jpg'
            # Write the updated data back to the JSON file
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=2)

# Directory containing the JSON files
json_directory = '.'

# Update 'imagePath' in all JSON files
update_imagepath(json_directory)