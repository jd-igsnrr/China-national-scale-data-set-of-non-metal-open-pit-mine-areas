import os
from pathlib import Path
from sklearn.model_selection import train_test_split

# Define the directory containing the files
data_dir = Path('images')

# Get a list of file paths
file_paths = [file for file in data_dir.glob('*') if file.is_file()]

# Split the file paths into training and validation sets (80% training, 20% validation)
train_paths, val_paths = train_test_split(file_paths, test_size=0.2, random_state=42)

# Save the absolute file paths to train.txt and val.txt
with open('train.txt', 'w') as train_file:
    train_file.writelines(f"{str(path.absolute())}\n" for path in train_paths)

with open('val.txt', 'w') as val_file:
    val_file.writelines(f"{str(path.absolute())}\n" for path in val_paths)