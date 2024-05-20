import geopandas as gpd

# Read two Shapefiles
gdf1 = gpd.read_file('input1.shp')
gdf2 = gpd.read_file('input2.shp')

# Use spatial join to find vectors in the first Shapefile that overlap with the second Shapefile
# Here, the 'sjoin' method is used with the default 'inner' join, which means only vectors present in both Shapefiles are retained
# The 'op' parameter is set to 'intersects', indicating that only spatially intersecting vectors are selected
# Note: Ensure both Shapefiles have the same coordinate system
gdf_joined = gpd.sjoin(gdf1, gdf2[['Province', 'geometry']], how='left', op='intersects')

# Inherit the 'Province' field from the second Shapefile to the corresponding vectors in the first Shapefile
# The result is already in gdf_joined, which can be further processed or saved as needed
gdf_joined = gdf_joined.drop(columns=['index_right'])  # Remove the automatically generated 'index_right' column, if present

# Save the modified first Shapefile
gdf_joined.to_file('output.shp', encoding='utf-8')