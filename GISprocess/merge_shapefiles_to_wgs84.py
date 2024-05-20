import geopandas as gpd
import pandas as pd
import glob
import os

# Set the folder path containing Shapefiles
folder_path = './finall'

# Use glob to find all Shapefiles
shapefiles = glob.glob(os.path.join(folder_path, "*.shp"))

# Read Shapefiles and convert CRS
gdf_list = []
for shp in shapefiles:
    gdf = gpd.read_file(shp)
    # Convert to WGS 84 CRS (EPSG:4326)
    gdf = gdf.to_crs(epsg=4326)
    gdf_list.append(gdf)

# Merge the GeoDataFrames
merged_gdf = gpd.GeoDataFrame(pd.concat(gdf_list, ignore_index=True))

# Save the merged Shapefile
output_path = 'finall.shp'
merged_gdf.to_file(output_path)