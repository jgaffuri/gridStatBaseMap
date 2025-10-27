import os
from qgis.core import (
    QgsProject,
    QgsMapSettings,
    QgsMapRendererCustomPainterJob,
    QgsRectangle,
    QgsPointXY
)
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QSize
from qgis.utils import iface

import numpy as np

def is_image_empty_np(image, white_threshold=254):
    """
    Checks if image is almost white everywhere.
    white_threshold: 0-255 value — higher means more lenient.
    """
    ptr = image.bits()
    ptr.setsize(image.byteCount())
    arr = np.frombuffer(ptr, np.uint8).reshape(image.height(), image.width(), 4)
    mean_value = arr[..., :3].mean()  # average RGB
    return mean_value > white_threshold


# --- Parameters ---
output_folder = "/home/juju/Bureau/tiles/"
#origin_point = [3946253, 2255080]
#scale = 25000
origin_point = [0, 6000000]
scale0 = 102400000
size_px = 256
dpi = 96

# get current projetc
project = QgsProject.instance()

# set map settings
settings = QgsMapSettings()
settings.setDestinationCrs(project.crs())
settings.setBackgroundColor(iface.mapCanvas().canvasColor())
settings.setOutputSize(QSize(size_px, size_px))
settings.setOutputDpi(dpi)
img_format = QImage.Format_ARGB32

# get layers: only the visible ones
layer_tree = project.layerTreeRoot()
ordered_layers = layer_tree.layerOrder()
visible_layers = [
    lyr for lyr in ordered_layers
    if layer_tree.findLayer(lyr.id()).isVisible()
]
settings.setLayers(visible_layers)

# https://tile.aaa.org/{z}/{x}/{y}.png
[x0,y0] = origin_point
nb_tiles0 = 1
for z in range(0, 11):

    scale = scale0 / 2 ** z
    nb_tiles = nb_tiles0 * 2 ** z
    size_m = (size_px * 0.0254 * scale) / dpi

    # check
    sc = settings.computeExtentForScale(QgsPointXY(1000000,3000000), scale)
    ddd = size_m - sc.xMaximum()+sc.xMinimum()
    assert ddd < 1e-9, "Inconsitent size_m: " + str(size_m) + " " + str(sc.xMaximum()-sc.xMinimum())

    for j in range(nb_tiles):
        x = x0 + j*size_m

        f = output_folder + "/" + str(z) + "/" + str(j) + "/"

        print("z=", z, str(j+1) + "/" + str(nb_tiles), "scale=", scale, "size_m=", size_m)

        for i in range(nb_tiles):
            y = y0 - (i+1)*size_m

            # set image geo extent
            settings.setExtent(QgsRectangle(x, y, x+size_m, y+size_m))

            # make image
            image = QImage(size_px, size_px, img_format)

            # paint image
            p = QPainter(image)
            job = QgsMapRendererCustomPainterJob(settings, p)
            job.start()
            job.waitForFinished()
            p.end()

            # skip if map empty
            if is_image_empty_np(image, white_threshold=254.999999999999): continue

            # create folder
            if not os.path.exists(f): os.makedirs(f)

            # save image
            output_path = output_folder + "/" + str(z) + "/" + str(j) + "_" + str(i)+".png"
            image.save(output_path, "PNG")
            output_path = f + str(i)+".png"
            image.save(output_path, "PNG")

print("done")



'''
# see https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/rastertools.html#generate-xyz-tiles-directory

import processing

params = {
          "OUTPUT_DIRECTORY":"/home/juju/Bureau/tiles",
          #Extent (xmin, xmax, ymin, ymax)
          #"EXTENT":"4300000,4400000,2700000,2800000 [EPSG:3035]",
          "EXTENT":"900000,6600000,900000,5500000 [EPSG:3035]",
          "ZOOM_MIN":3,
          "ZOOM_MAX":12,
          "DPI":96,
          "ANTIALIAS":True,
          "TILE_HEIGHT":256,"TILE_WIDTH":256,
          "TILE_FORMAT":0,
          "TMS_CONVENTION":False,
          "BACKGROUND_COLOR":"rgba( 0, 0, 0, 0.00 )",
          "HTML_ATTRIBUTION":"",
          "HTML_OSM":False,
          "HTML_TITLE":"",
          "METATILESIZE":4,
          "OUTPUT_HTML":"",
          "QUALITY":75
          }
processing.run("native:tilesxyzdirectory", params)
'''
