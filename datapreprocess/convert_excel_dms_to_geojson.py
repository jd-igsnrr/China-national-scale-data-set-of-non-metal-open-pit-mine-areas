import json
import openpyxl

def dms_to_decimal(d, m, s):
    # Convert degrees, minutes, and seconds (DMS) to decimal degrees
    return d + (m / 60.0) + (s / 3600.0)

def parse_coordinates(coord_string):
    # Parse a coordinate string formatted in DMS separated by dashes and semicolons into decimal degrees
    coords = []
    for point in coord_string.split(';'):
        dms_parts = point.split('-')
        lon = dms_to_decimal(float(dms_parts[0]), float(dms_parts[1]), float(dms_parts[2]))
        lat = dms_to_decimal(float(dms_parts[3]), float(dms_parts[4]), float(dms_parts[5]))
        coords.append([lon, lat])
    # Ensure the polygon is closed by adding the first point at the end
    if coords and coords[0] != coords[-1]:
        coords.append(coords[0])
    return coords

# Read the Excel file
wb = openpyxl.load_workbook('./locations.xlsx')
sheet = wb.active

# Initialize an empty GeoJSON FeatureCollection
geojson_feature_collection = {
    "type": "FeatureCollection",
    "features": []
}

# Iterate over the rows in the Excel sheet
for row in sheet.iter_rows(min_row=1, max_col=1, values_only=True):
    coord_string = row[0]
    if coord_string:  # Check if the cell is not empty
        # Parse the coordinates
        coordinates = parse_coordinates(coord_string)

        # Construct GeoJSON feature
        geojson_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            },
            "properties": {}
        }

        # Add the feature to the FeatureCollection
        geojson_feature_collection["features"].append(geojson_feature)

# Save the GeoJSON FeatureCollection to a file
with open('polygons.geojson', 'w') as f:
    json.dump(geojson_feature_collection, f)