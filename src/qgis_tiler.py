import sys
import os
import numpy as np
from datetime import datetime
from math import floor, ceil
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




def tile_from_qgis_project(project_path,
                           output_folder,
                           resolution0,
                           extent, # [xmin,ymin,xmax,ymax]
                           origin_point = [0, 0],
                           z_min=0, z_max=3,
                           tile_size_px = 256,
                           img_format = QImage.Format_RGB32,
                           skip_white_image = True,
                           backgroundcolor = QColor(255, 255, 255),
                           ):
    """
    Create a XYZ slippy map tile set from a QGIS project, to be used with https://tile.aaa.org/{z}/{x}/{y}.png URL pattern.

    Args:
        project_path (str): The QGIS project file path.
        output_folder (str): The output folder for the tiles.
        resolution0 (number): The resolution (meters per pixel) at zoom level 0.
        extent (array): The extent [xmin, ymin, xmax, ymax] to cover with tiles.
        z_min (int, optional): The minimum zoom level to produce. Defaults to 0.
        z_max (int, optional): The maxipum zoom level to produce. Defaults to 3.
        tile_size_px (int, optional): The tile size, in pixel number. Defaults to 256.
        img_format (QImage, optional): The image format. Defaults to QImage.Format_RGB32.
        skip_white_image (bool, optional): Set to True if white images do not need to be produced. Defaults to True.
        backgroundcolor (QColor, optional): The map background color. Defaults to QColor(255, 255, 255).
    """
    # open QGIS
    qgs = QgsApplication([], False)
    qgs.setPrefixPath(sys.prefix, True)
    qgs.initQgis()

    try:

        # read qgis project
        project = QgsProject.instance()
        project.read(project_path)

        # define map settings
        settings = QgsMapSettings()
        settings.setDestinationCrs(project.crs())
        settings.setBackgroundColor(backgroundcolor)
        settings.setOutputSize(QSize(tile_size_px, tile_size_px))
        settings.setOutputDpi(90.714) # it seems to work :-)

        # get layers: only the visible ones
        layer_tree = project.layerTreeRoot()
        ordered_layers = layer_tree.layerOrder()
        visible_layers = [
            lyr for lyr in ordered_layers
            if layer_tree.findLayer(lyr.id()).isVisible()
        ]
        settings.setLayers(visible_layers)

        # parse origin point and extent
        [x0,y0] = origin_point
        [x_min, y_min, x_max, y_max] = extent

        # handle zoom levels
        for z in range(z_min, z_max+1):

            # compute zoom related parameters
            pix_size_m = resolution0 / 2 ** z
            scale = pix_size_m / 0.00028
            tile_size_m = tile_size_px * pix_size_m
            #size_m = (size_px * 0.0254 * scale) / dpi

            # check that...
            sc = settings.computeExtentForScale(QgsPointXY(0, 0), scale)
            ddd = tile_size_m - sc.xMaximum()+sc.xMinimum()
            assert ddd < 1e-9, "Inconsitent size_m: " + str(tile_size_m) + " " + str(sc.xMaximum()-sc.xMinimum())

            # compute tile indexes
            # columns
            j_min = floor((x_min-x0)/tile_size_m)
            j_max = ceil((x_max-x0)/tile_size_m)
            # rows
            i_min = floor((y0-y_max)/tile_size_m)
            i_max = ceil((y0-y_min)/tile_size_m)

            # columns
            for j in range(j_min, j_max):

                # tile column lower left corner x coordinate
                x = x0 + j*tile_size_m

                # output folder
                f = output_folder + "/" + str(z) + "/" + str(j) + "/"

                print(datetime.now(), "z=", z, str(j+1-j_min) + "/" + str(j_max-j_min), "scale=", scale, "resolution=", pix_size_m, "m")

                # rows
                for i in range(i_min, i_max):

                    # tile row lower left corner y coordinate
                    y = y0 - (i+1)*tile_size_m

                    # set image geo extent
                    settings.setExtent(QgsRectangle(x, y, x+tile_size_m, y+tile_size_m))

                    # make image
                    image = QImage(tile_size_px, tile_size_px, img_format)

                    # paint image
                    p = QPainter(image)
                    job = QgsMapRendererCustomPainterJob(settings, p)
                    job.start()
                    job.waitForFinished()
                    p.end()

                    # skip if image is empty
                    if skip_white_image and is_image_empty_np(image): continue

                    # create folder, if needed
                    if not os.path.exists(f): os.makedirs(f)

                    # save image
                    output_path = f + str(i)+".png"
                    image.save(output_path, "PNG")

    finally:
        # close QGIS
        qgs.exitQgis()







'''
def tile_from_qgis_project_old(project_path, output_folder, origin_point = [0, 0],
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

'''

