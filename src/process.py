from qgis_tiler import tile_from_qgis_project


'''
tile_from_qgis_project(
    project_path = "/home/juju/workspace/gridStatBaseMap/src/elevation.qgz",
    output_folder = "/home/juju/Bureau/tiles_elevation/",
    resolution0 = 114688,
    extent = [0, 0, 8000000, 6000000],
    #extent = [3940000, 2270000, 3947000, 2277000],
    #extent = [4060000, 2960000, 4080000, 2980000],
    origin_point = [0, 6000000],
    tile_size_px = 256, # 512 256
    z_min = 12,
    z_max = 12,
    # Format_RGB16 Format_RGB32 Format_Grayscale16, # see on https://doc.qt.io/qt-6/qimage.html
    img_format = QImage.Format_RGB32,
)
'''


tile_from_qgis_project(
    project_path = "/home/juju/workspace/gridStatBaseMap/src/road.qgz",
    output_folder = "/home/juju/Bureau/tiles_road/",
    resolution0 = 114688,
    extent = [0, 0, 8000000, 6000000],
    origin_point = [0, 6000000],
    tile_size_px = 512, # 512 256
    z_min = 0,
    z_max = 14,
    # Format_RGB16 Format_RGB32 Format_Grayscale16, # see on https://doc.qt.io/qt-6/qimage.html
    img_format = QImage.Format_Grayscale16,
)

