import geopandas as gpd

# Read the Shapefile to be clipped
target_shp = gpd.read_file("shapefile1.shp")

# Read the Shapefile used for clipping
clip_shp = gpd.read_file("shapefile2.shp")

# Match the Coordinate Reference System (CRS) of both Shapefiles
target_shp = target_shp.to_crs(clip_shp.crs)

# Apply a buffer(0) to the geometries to attempt to fix topology errors
target_shp['geometry'] = target_shp.buffer(0)
clip_shp['geometry'] = clip_shp.buffer(0)

# Perform the clipping operation
clipped_shp = gpd.clip(target_shp, clip_shp)

# Save the clipped Shapefile
clipped_shp.to_file("output.shp", encoding='utf-8')