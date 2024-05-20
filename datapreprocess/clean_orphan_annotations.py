from pathlib import Path

# Define the directories
ann_dir = Path('annotation')  # Directory for annotation files
images_dir = Path('images')  # Directory for image files

# Create a set of image file names without extension
image_files = {file.stem for file in images_dir.glob('*.*')}  # Extract names without extensions for comparison

# Iterate over annotation files and remove those without a corresponding image file
for ann_file in ann_dir.glob('*.*'):
    if ann_file.stem not in image_files:
        ann_file.unlink()  # This will delete the file if there is no corresponding image