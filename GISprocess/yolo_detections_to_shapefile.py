from osgeo import ogr, osr
import os

def parse_jgw(jgw_file):
    # Read a .jgw (world file) and return its transformation parameters as a list of floats
    with open(jgw_file, 'r') as file:
        lines = file.readlines()
        return [float(value.strip()) for value in lines]

def parse_yolo_txt(yolo_txt_file, transform_params):
    # Parse YOLO format detection files and apply transformation parameters to convert to geographic coordinates
    detections = []
    with open(yolo_txt_file, 'r') as file:
        for line in file:
            class_id, x_center, y_center, width, height = [float(value) * 1024 for value in line.split()][:5]
            top_left_x = (x_center - width / 2) * transform_params[0] + transform_params[4]
            top_left_y = (y_center + height / 2) * transform_params[3] + transform_params[5]
            bottom_right_x = (x_center + width / 2) * transform_params[0] + transform_params[4]
            bottom_right_y = (y_center - height / 2) * transform_params[3] + transform_params[5]
            detections.append((class_id, top_left_x, top_left_y, bottom_right_x, bottom_right_y))
    return detections

def add_detections_to_shapefile(detections, layer):
    # Add detections to a shapefile layer as polygon features
    for detection in detections:
        class_id, top_left_x, top_left_y, bottom_right_x, bottom_right_y = detection
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(top_left_x, top_left_y)
        ring.AddPoint(bottom_right_x, top_left_y)
        ring.AddPoint(bottom_right_x, bottom_right_y)
        ring.AddPoint(top_left_x, bottom_right_y)
        ring.AddPoint(top_left_x, top_left_y)
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        feature = ogr.Feature(layer.GetLayerDefn())
        feature.SetGeometry(poly)
        feature.SetField('class_id', int(class_id))
        layer.CreateFeature(feature)
        feature = None

def get_spatial_reference_from_prj(prj_file):
    # Extract spatial reference from a .prj file
    with open(prj_file, 'r') as file:
        prj_txt = file.read()
        srs = osr.SpatialReference()
        srs.ImportFromWkt(prj_txt)
        return srs

detection_folder = 'result/labels'
jgw_folder = 'jgw'
prj_file_path = 'mine.prj'
output_shp_file_path = 'output.shp'

srs = get_spatial_reference_from_prj(prj_file_path)

driver = ogr.GetDriverByName('ESRI Shapefile')
if os.path.exists(output_shp_file_path):
    driver.DeleteDataSource(output_shp_file_path)
data_source = driver.CreateDataSource(output_shp_file_path)
layer = data_source.CreateLayer('detections', srs, ogr.wkbPolygon)
layer.CreateField(ogr.FieldDefn('class_id', ogr.OFTInteger))

for yolo_file in os.listdir(detection_folder):
    if yolo_file.endswith('.txt'):
        base_name = os.path.splitext(yolo_file)[0]
        jgw_file = os.path.join(jgw_folder, base_name + '.jgw')
        if os.path.exists(jgw_file):
            transform_params = parse_jgw(jgw_file)
            yolo_txt_file = os.path.join(detection_folder, yolo_file)
            detections = parse_yolo_txt(yolo_txt_file, transform_params)
            add_detections_to_shapefile(detections, layer)
        else:
            print(f"No corresponding JGW file found for {yolo_file}")

data_source = None