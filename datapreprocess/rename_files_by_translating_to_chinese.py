import os

# Step 1: Read the mapping file and build a translation dictionary
translation_dict = {}
with open('chinese_pinyin_mapping.txt', 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():  # Ensure the line is not empty
            chinese, english = line.strip().split()
            translation_dict[english] = chinese

# Step 2: Iterate over all files in the folder
folder_path = 'train/labels'  # Set your folder path
for filename in os.listdir(folder_path):
    base_name, extension = os.path.splitext(filename)
    # Split the filename
    name_parts = base_name.split('_')
    # Step 3: Replace the English parts of the filename
    new_name_parts = [translation_dict.get(part, part) for part in name_parts]
    new_base_name = '_'.join(new_name_parts)
    new_name = f"{new_base_name}{extension}"
    # Step 4: Rename the file
    if new_name != filename:
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_name))