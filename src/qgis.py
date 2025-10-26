from qgis.core import (
    QgsProject,
    QgsMapSettings,
    QgsMapRendererCustomPainterJob,
    QgsRectangle
)
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QSize

# --- Parameters ---
output_path = "/home/juju/Bureau/tiles/export.png"
xmin, ymin, xmax, ymax = 3700000, 2700000, 3800000, 2800000
scale = 100000
width_px = 256
height_px = 256

# --- Build map settings ---
settings = QgsMapSettings()
settings.setLayers(QgsProject.instance().mapLayers().values())
#settings.setBackgroundColor(Qt.white)

# Define extent
extent = QgsRectangle(xmin, ymin, xmax, ymax)
settings.setExtent(extent)

# Set output size (in pixels)
settings.setOutputSize(QSize(width_px, height_px))

# Optionally fix scale
#settings.setScale(scale)
settings.setOutputDpi(96)


# --- Render to image ---
image = QImage(width_px, height_px, QImage.Format_ARGB32)
image.fill(Qt.white)

p = QPainter(image)
job = QgsMapRendererCustomPainterJob(settings, p)
job.start()
job.waitForFinished()
p.end()

image.save(output_path, "PNG")





'''
# works ! with layout


from qgis.core import (
    QgsProject,
    QgsLayoutExporter,
    QgsLayoutItemMap,
    QgsLayout,
    QgsLayoutPoint,
    QgsLayoutSize,
    QgsPrintLayout,
    QgsRectangle
)
from qgis.PyQt.QtCore import QSizeF
import math

output_path = "/home/juju/Bureau/tiles/export.png"
xmin, ymin, xmax, ymax = 3700000, 2700000, 3800000, 2800000
extent = QgsRectangle(xmin, ymin, xmax, ymax)
scale = 1000000
image_width = 256
image_height = 256
#dpi = 300

# load project
project = QgsProject.instance()

# --- Create layout ---
layout = QgsPrintLayout(project)
layout.initializeDefaults()
layout.setName("ExportLayout")

# --- Add a map item ---
map_item = QgsLayoutItemMap(layout)
map_item.setRect(0, 0, 200, 200)

# Set extent and scale
map_item.setExtent(extent)
map_item.setScale(scale)

# Define map item size (in mm)
# E.g., 100 mm × 100 mm square
map_item.attemptMove(QgsLayoutPoint(5, 5))
map_item.attemptResize(QgsLayoutSize(100, 100))
layout.addLayoutItem(map_item)

# --- Export to PNG ---
exporter = QgsLayoutExporter(layout)
settings = QgsLayoutExporter.ImageExportSettings()
#settings.dpi = dpi
settings.width = image_width
settings.height = image_height

result = exporter.exportToImage(output_path, settings)

print(f"Export done → {output_path}, result code: {result}")

'''





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
