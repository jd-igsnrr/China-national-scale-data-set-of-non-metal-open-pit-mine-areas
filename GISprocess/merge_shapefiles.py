import geopandas as gpd
import pandas as pd

# Read two Shapefiles
gdf1 = gpd.read_file('shapefile1.shp')
gdf2 = gpd.read_file('shapefile2.shp')

# Merge GeoDataFrames
merged_gdf = gpd.GeoDataFrame(pd.concat([gdf1, gdf2], ignore_index=True))

# Save the merged GeoDataFrame as a new Shapefile
merged_gdf.to_file('output.shp')