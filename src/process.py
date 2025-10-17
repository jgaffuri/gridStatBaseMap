# Initialisation de QGIS
from init_qgis import qgs, QgsProject, QgsMapSettings, QgsMapRendererParallelJob, QgsRasterFileWriter, QgsRectangle, QSize
import sys

def export_map_to_geotiff(project_path, output_path, scale, extent):
    """Exporte la carte d'un projet QGIS au format GeoTIFF."""
    project = QgsProject.instance()
    project.read(project_path)

    map_settings = QgsMapSettings()
    map_settings.setLayers(project.mapLayers().values())
    map_settings.setDestinationCrs(project.crs())
    map_settings.setExtent(QgsRectangle(*extent))
    map_settings.setScale(scale)
    map_settings.setOutputSize(QSize(800, 600))

    job = QgsMapRendererParallelJob(map_settings)
    job.start()
    job.waitForFinished()

    image = job.renderedImage()
    writer = QgsRasterFileWriter(output_path)
    writer.writeRaster(
        image,
        map_settings.extent().width(),
        map_settings.extent().height(),
        map_settings.extent(),
        map_settings.destinationCrs()
    )
    print(f"Export terminé : {output_path}")



scales = []
sca = 102400000
for i in range(5): #13
    scales.append(sca)
    sca /= 2

print(scales)




