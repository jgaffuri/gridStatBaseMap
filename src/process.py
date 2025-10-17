# Initialisation de QGIS
from init_qgis import qgs, QgsLayoutExporter, QgsLayoutItemMap, QgsPrintLayout, QgsApplication, QgsProject, QgsMapSettings, QgsMapRendererParallelJob, QgsRasterFileWriter, QgsRectangle, QSize
import sys


def export_map_to_geotiff(project_path, output_path, extent, scale):
    """
    Exporte la carte d'un projet QGIS au format GeoTIFF.

    :param project_path: Chemin vers le fichier .qgz ou .qgs
    :param output_path: Chemin de sortie pour le GeoTIFF
    :param extent: Emprise sous forme de tuple (xmin, ymin, xmax, ymax)
    :param scale: Denominateur du facteur d'échelle
    """
    # Initialiser QGIS (nécessaire pour les scripts autonomes)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    # Charger le projet
    project = QgsProject.instance()
    project.read(project_path)

    # Créer un layout
    layout = QgsPrintLayout(project)
    layout.initializeDefaults()

    # Ajouter une carte au layout
    map = QgsLayoutItemMap(layout)
    map.setExtent(QgsRectangle(*extent))
    map.setScale(scale)
    layout.addLayoutItem(map)

    # Exporter en GeoTIFF
    exporter = QgsLayoutExporter(layout)
    exporter.exportToImage(output_path, QgsLayoutExporter.ImageExportSettings())

    print(f"Export terminé : {output_path}")

    qgs.exitQgis()


'''
scales = []
sca = 102400000
for i in range(5): #13
    scales.append(sca)
    sca /= 2

print(scales)
'''

scale = 1000000
# (xmin, ymin, xmax, ymax)
extent = (3700000, 2700000, 3710000, 2710000)
export_map_to_geotiff("src/project.qgz", "tmp/aaa.tiff", extent, scale)



#
qgs.exitQgis()
