from osgeo import ogr, osr
import os
import math

def split_shapefile(input_shp, output_root_dir, num_splits=5):
    # Open the original Shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    input_ds = driver.Open(input_shp, 0)  # 0 means read-only
    input_lyr = input_ds.GetLayer()
    
    # Get the spatial reference of the original Shapefile
    input_srs = input_lyr.GetSpatialRef()

    # Calculate the total number of features and the number of features per split
    feature_count = input_lyr.GetFeatureCount()
    features_per_split = math.ceil(feature_count / num_splits)

    # Create new Shapefiles and allocate features
    for i in range(num_splits):
        # Create a corresponding directory for each new Shapefile
        output_dir = os.path.join(output_root_dir, f"split_{i+1}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create a new Shapefile
        output_shp_path = os.path.join(output_dir, "part.shp")
        if os.path.exists(output_shp_path):
            driver.DeleteDataSource(output_shp_path)
        output_ds = driver.CreateDataSource(output_shp_path)
        output_lyr = output_ds.CreateLayer("part", input_srs, geom_type=input_lyr.GetGeomType())
        
        # Copy fields
        in_layer_defn = input_lyr.GetLayerDefn()
        for j in range(in_layer_defn.GetFieldCount()):
            field_defn = in_layer_defn.GetFieldDefn(j)
            output_lyr.CreateField(field_defn)
        
        # Allocate features to the new Shapefile
        for k in range(features_per_split):
            feature_index = i * features_per_split + k
            if feature_index < feature_count:
                input_lyr.SetNextByIndex(feature_index)
                in_feat = input_lyr.GetNextFeature()
                out_feat = ogr.Feature(output_lyr.GetLayerDefn())
                out_feat.SetGeometry(in_feat.GetGeometryRef().Clone())
                for j in range(in_layer_defn.GetFieldCount()):
                    out_feat.SetField(in_layer_defn.GetFieldDefn(j).GetNameRef(), in_feat.GetField(j))
                output_lyr.CreateFeature(out_feat)
                out_feat = None
            else:
                break
        
        # Close the data source
        output_ds = None

input_shp = 'input.shp'
output_root_dir = 'output.shp'
split_shapefile(input_shp, output_root_dir)