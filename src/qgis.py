
import processing

# see https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/rastertools.html#generate-xyz-tiles-directory

params = {"ANTIALIAS":True,
          "BACKGROUND_COLOR":"rgba( 0, 0, 0, 0.00 )",
          "DPI":96,
          "EXTENT":"4438044.965100000,4441476.558800000,2780393.530700000,2784484.856900000 [EPSG:3035]",
          "HTML_ATTRIBUTION":"",
          "HTML_OSM":False,"HTML_TITLE":"","METATILESIZE":4,
          "OUTPUT_DIRECTORY":"/home/juju/Bureau/tiles",
          "OUTPUT_HTML":"","QUALITY":75,
          "TILE_FORMAT":0,
          "TILE_HEIGHT":256,"TILE_WIDTH":256,
          "TMS_CONVENTION":False,
          "ZOOM_MAX":12,"ZOOM_MIN":9
          }
processing.run("native:tilesxyzdirectory", params)

