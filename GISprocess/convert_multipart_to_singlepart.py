from osgeo import ogr, osr
import os

def multipart_to_singlepart(input_shp, output_shp):
    # Open the original multipart Shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    input_ds = driver.Open(input_shp, 0)  # 0 means read-only
    input_lyr = input_ds.GetLayer()
    
    # Get the spatial reference of the original Shapefile
    input_srs = input_lyr.GetSpatialRef()

    # Create a new Shapefile to store singlepart features
    if os.path.exists(output_shp):
        driver.DeleteDataSource(output_shp)
    output_ds = driver.CreateDataSource(output_shp)
    output_lyr = output_ds.CreateLayer(input_lyr.GetName(), input_srs, geom_type=ogr.wkbPolygon)

    # Copy fields
    in_layer_defn = input_lyr.GetLayerDefn()
    for i in range(in_layer_defn.GetFieldCount()):
        field_defn = in_layer_defn.GetFieldDefn(i)
        output_lyr.CreateField(field_defn)

    # Iterate through each feature in the original Shapefile
    for in_feat in input_lyr:
        geom = in_feat.GetGeometryRef()
        # For each multipart feature, break it into singlepart features
        if geom.GetGeometryType() == ogr.wkbMultiPolygon:
            for geom_part in geom:
                out_feat = ogr.Feature(output_lyr.GetLayerDefn())
                out_feat.SetGeometry(geom_part.Clone())  # Clone the geometry
                # Copy attributes
                for i in range(in_layer_defn.GetFieldCount()):
                    out_feat.SetField(in_layer_defn.GetFieldDefn(i).GetNameRef(), in_feat.GetField(i))
                output_lyr.CreateFeature(out_feat)
                out_feat = None
        else:
            out_feat = ogr.Feature(output_lyr.GetLayerDefn())
            out_feat.SetGeometry(geom.Clone())  # Clone the geometry
            # Copy attributes
            for i in range(in_layer_defn.GetFieldCount()):
                out_feat.SetField(in_layer_defn.GetFieldDefn(i).GetNameRef(), in_feat.GetField(i))
            output_lyr.CreateFeature(out_feat)
            out_feat = None

    # Close the data sources
    input_ds = None
    output_ds = None

# Use the function
input_shp = 'input.shp'
output_shp = 'output.shp'
multipart_to_singlepart(input_shp, output_shp)