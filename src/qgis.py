
# see https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/rastertools.html#generate-xyz-tiles-directory
#   --extent="3700000,2700000,3710000,2710000 [EPSG:3035]" \

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

