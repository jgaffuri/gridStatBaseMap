import sys
import os
import numpy as np
from datetime import datetime
from qgis.core import (
    QgsApplication,
    QgsProject,
    QgsMapSettings,
    QgsMapRendererCustomPainterJob,
    QgsRectangle,
    QgsPointXY
)
from PyQt5.QtGui import QImage, QPainter, QColor
from PyQt5.QtCore import QSize


#TODO: instead of nb_tiles0, define bbox. For EPSG:3035, use 0,0,8000000,6000000
#TODO: define resolutions instead of scales ?
#TODO: adopt new scheme




def tile_from_qgis_project(project_path, output_folder, origin_point = [0, 0],
                           z_min=0, z_max=3,
                           scale0 = 102400000, nb_tiles0 = 1,
                           tile_size_px = 256, img_format = QImage.Format_RGB32, skip_white_image = True):

    def is_image_empty_np(image: QImage, white_threshold=255):
        """
        Checks if image is almost white everywhere.
        Works with Grayscale16, Grayscale8, RGB32, ARGB32, etc.
        """
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        buf = np.frombuffer(ptr, np.uint8)

        if image.format() in (QImage.Format_ARGB32, QImage.Format_RGB32):
            arr = buf.reshape(image.height(), image.width(), 4)
            mean_value = arr[..., :3].mean()
        elif image.format() == QImage.Format_RGB888:
            arr = buf.reshape(image.height(), image.width(), 3)
            mean_value = arr.mean()
        elif image.format() in (QImage.Format_Grayscale8,):
            arr = buf.reshape(image.height(), image.width())
            mean_value = arr.mean()
        elif image.format() in (QImage.Format_Grayscale16,):
            # two bytes per pixel, need to view as uint16
            arr = buf.view(np.uint16).reshape(image.height(), image.width())
            # Scale 16-bit grayscale to 0–255 range
            arr8 = (arr / 257).astype(np.uint8)  # 65535/255 ≈ 257
            mean_value = arr8.mean()
        else:
            raise ValueError(f"Unsupported QImage format: {image.format()}")

        return mean_value >= white_threshold

    # read project
    project = QgsProject.instance()
    project.read(project_path)


    # set map settings
    settings = QgsMapSettings()
    settings.setDestinationCrs(project.crs())
    settings.setBackgroundColor(QColor(255, 255, 255))
    settings.setOutputSize(QSize(tile_size_px, tile_size_px))
    settings.setOutputDpi(90.714)

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
    for z in range(z_min, z_max+1):

        scale = scale0 / 2 ** z
        nb_tiles = nb_tiles0 * 2 ** z
        pix_size_m = scale * 0.00028
        #size_m = (size_px * 0.0254 * scale) / dpi
        size_m = tile_size_px * pix_size_m

        # check
        sc = settings.computeExtentForScale(QgsPointXY(0, 0), scale)
        ddd = size_m - sc.xMaximum()+sc.xMinimum()
        assert ddd < 1e-9, "Inconsitent size_m: " + str(size_m) + " " + str(sc.xMaximum()-sc.xMinimum())

        #print("z=", z, "scale=", scale, "resolution=", pix_size_m, "m")

        for j in range(nb_tiles):
            x = x0 + j*size_m

            # output folder
            f = output_folder + "/" + str(z) + "/" + str(j) + "/"

            print(datetime.now(), "z=", z, str(j+1) + "/" + str(nb_tiles), "scale=", scale, "resolution=", pix_size_m, "m")

            for i in range(nb_tiles):
                y = y0 - (i+1)*size_m

                # set image geo extent
                settings.setExtent(QgsRectangle(x, y, x+size_m, y+size_m))

                # make image
                image = QImage(tile_size_px, tile_size_px, img_format)

                # paint image
                p = QPainter(image)
                job = QgsMapRendererCustomPainterJob(settings, p)
                job.start()
                job.waitForFinished()
                p.end()

                # skip if map empty
                if skip_white_image and is_image_empty_np(image): continue

                # create folder, if needed
                if not os.path.exists(f): os.makedirs(f)

                # save image
                output_path = f + str(i)+".png"
                image.save(output_path, "PNG")

                # for debugging
                #output_path = output_folder + "/" + str(z) + "/" + str(j) + "_" + str(i)+".png"
                #image.save(output_path, "PNG")




# Initialize QGIS
qgs = QgsApplication([], False)
qgs.setPrefixPath(sys.prefix, True)
qgs.initQgis()


tile_from_qgis_project(
    project_path= "/home/juju/workspace/gridStatBaseMap/src/project.qgz",
    output_folder = "/home/juju/Bureau/tiles/",
    origin_point = [0, 6000000],
    scale0 = 51200000, nb_tiles0 = 1, tile_size_px = 512,
    z_min = 9,
    z_max = 11,
    img_format = QImage.Format_Grayscale16,
)

# close
qgs.exitQgis()

