from osgeo import ogr, osr
import os

def create_buffer(input_shp, output_shp, buffer_dist):
    # Open the input shapefile
    input_ds = ogr.Open(input_shp)
    input_lyr = input_ds.GetLayer()
    
    # Create the output shapefile
    shp_driver = ogr.GetDriverByName('ESRI Shapefile')
    if os.path.exists(output_shp):
        shp_driver.DeleteDataSource(output_shp)
    output_ds = shp_driver.CreateDataSource(output_shp)
    
    # Get spatial reference from input layer
    spatial_ref = input_lyr.GetSpatialRef()
    
    # Create output layer
    output_lyr = output_ds.CreateLayer('buffer', spatial_ref, ogr.wkbPolygon)
    
    # Add fields from the input layer to the output layer
    input_lyr_defn = input_lyr.GetLayerDefn()
    for i in range(0, input_lyr_defn.GetFieldCount()):
        field_defn = input_lyr_defn.GetFieldDefn(i)
        output_lyr.CreateField(field_defn)
    
    # Buffer operation
    for feature in input_lyr:
        input_geom = feature.GetGeometryRef()
        buffer_geom = input_geom.Buffer(buffer_dist)
        
        # Create a new feature, set its geometry and attributes
        out_feature = ogr.Feature(output_lyr.GetLayerDefn())
        out_feature.SetGeometry(buffer_geom)
        for i in range(0, input_lyr_defn.GetFieldCount()):
            out_feature.SetField(input_lyr_defn.GetFieldDefn(i).GetNameRef(), feature.GetField(i))
        output_lyr.CreateFeature(out_feature)
        out_feature = None
    
    # Cleanup
    input_ds = None
    output_ds = None

input_shp = 'buffer/lastone_single.shp'
output_shp = './buffer/goodjob.shp'
buffer_dist = -0.00009  

create_buffer(input_shp, output_shp, buffer_dist)