from pathlib import Path
import os

# Define the directories
images_dir = Path('images')  # Directory for images
labels_dir = Path('labels')  # Directory for label files
test_dir = Path('test')  # Directory to store images without corresponding labels

# Create a set of label file names without extension
label_files = {file.stem for file in labels_dir.glob('*')}  # Extract names without extensions for comparison

# Iterate over image files and remove those without a corresponding label file
for image_file in images_dir.glob('*'):
    if image_file.stem not in label_files:
        new_path = test_dir / image_file.name
        # Move the file to the test directory if there is no corresponding label file
        image_file.rename(new_path)