from qgis.core import (
    QgsProject,
    QgsLayoutExporter,
    QgsLayoutItemMap,
    QgsLayout,
    QgsPrintLayout,
    QgsRectangle
)
from qgis.PyQt.QtCore import QSizeF
import math

# --- Parameters ---
output_path = "/path/to/output_map.png"

# Define extent (square)
xmin, ymin, xmax, ymax = 500000, 6500000, 501000, 6501000  # Example (1 km x 1 km)
extent = QgsRectangle(xmin, ymin, xmax, ymax)

scale = 5000             # e.g. 1:5000
image_width = 1000       # in pixels
image_height = 1000      # in pixels (square output)

# --- Load project ---
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
settings.dpi = 300
settings.width = image_width
settings.height = image_height

result = exporter.exportToImage(output_path, settings)

print(f"Export done → {output_path}, result code: {result}")




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
