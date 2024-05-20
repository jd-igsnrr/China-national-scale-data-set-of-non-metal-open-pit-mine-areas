import geopandas as gpd
import pandas as pd

# 1. Read the Shapefile
gdf = gpd.read_file("input.shp")

# If the coordinate system is geographic, convert it to a projected system (EPSG:3857) for accurate area and length calculations
if gdf.crs.is_geographic:
    gdf = gdf.to_crs(epsg=3857)

# 2. Group by the 'Province' field
grouped = gdf.groupby('Province')

# 3. Calculate the total length, total area, and number of vectors for each group
results = []
for name, group in grouped:
    length_sum = group.geometry.length.sum()  # Calculate total length
    area_sum = group.geometry.area.sum()  # Calculate total area
    vector_count = len(group)  # Count the number of vectors
    results.append({'Province': name, 'Total Length (m)': length_sum, 'Total Area (sq m)': area_sum, 'Vector Count': vector_count})

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# 4. Save as CSV
results_df.to_csv("output.csv", index=False, encoding='utf-8-sig')