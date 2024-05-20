import json
import os
from pathlib import Path

# Function to convert LabelMe rectangle to YOLO bounding box format
def rectangle_to_yolo_bbox(rectangle, image_width, image_height):
    # Calculate the bounding box
    x_min = min([point[0] for point in rectangle])
    x_max = max([point[0] for point in rectangle])
    y_min = min([point[1] for point in rectangle])
    y_max = max([point[1] for point in rectangle])
    
    x_center = ((x_min + x_max) / 2) / image_width
    y_center = ((y_min + y_max) / 2) / image_height
    bbox_width = (x_max - x_min) / image_width
    bbox_height = (y_max - y_min) / image_height
    
    return x_center, y_center, bbox_width, bbox_height

# Define source and target directories
src_dir = Path('./annotation/')
target_dir = Path('./labels/')
target_dir.mkdir(parents=True, exist_ok=True)

# Dictionary to map label names to YOLO class indices
label_to_index = {
    'label_name_1': 0,
    'label_name_2': 1,
    # Add more labels as needed
}

# Iterate over the JSON files in the source directory
for json_file in src_dir.glob('*.json'):
    # Read the JSON file
    with open(json_file) as f:
        data = json.load(f)
    
    # Extract image dimensions
    image_width = data['imageWidth']
    image_height = data['imageHeight']
    
    # Prepare the content for the YOLO annotation file
    yolo_annotations = []
    for shape in data['shapes']:
        if shape['shape_type'] != 'rectangle':
            continue  # Skip non-rectangle annotations
        label_index = 1  # This should map from `label_to_index`, example used directly for simplicity
        if label_index is None:
            continue  # Skip if label is not in the dictionary
        # Convert LabelMe rectangle to YOLO bbox
        bbox = rectangle_to_yolo_bbox(shape['points'], image_width, image_height)
        yolo_annotations.append(f"{label_index} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}")
    
    # Write the YOLO annotations to a new text file in the target directory
    yolo_filename = target_dir / (json_file.stem + '.txt')
    with open(yolo_filename, 'w') as f:
        f.write('\n'.join(yolo_annotations))