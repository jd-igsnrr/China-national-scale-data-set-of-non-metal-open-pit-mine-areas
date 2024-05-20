import geopandas as gpd

# Read two Shapefiles
gdf1 = gpd.read_file('shapefile1.shp')
gdf2 = gpd.read_file('shapefile2.shp')

# Ensure both GeoDataFrames use the same Coordinate Reference System (CRS)
gdf2 = gdf2.to_crs(gdf1.crs)

# Calculate the intersection
intersection_gdf = gpd.overlay(gdf1, gdf2, how='intersection')

# Save the intersection result to a new Shapefile
intersection_gdf.to_file('intersection_shapefile.shp')