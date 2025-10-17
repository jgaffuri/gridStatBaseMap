# Initialisation de QGIS
from init_qgis import qgs, QgsApplication, QgsProject, QgsMapSettings, QgsMapRendererParallelJob, QgsRasterFileWriter, QgsRectangle, QSize
import sys

'''
def export_map_to_geotiff(project_path, output_path, scale, extent):
    """Exporte la carte d'un projet QGIS au format GeoTIFF."""
    project = QgsProject.instance()
    project.read(project_path)

    map_settings = QgsMapSettings()
    map_settings.setLayers(project.mapLayers().values())
    map_settings.setDestinationCrs(project.crs())
    map_settings.setExtent(QgsRectangle(*extent))
    #map_settings.setScale(scale)
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
'''


def export_map_to_geotiff(project_path, output_path, extent, dpi=96):
    """
    Exporte la carte d'un projet QGIS au format GeoTIFF.

    :param project_path: Chemin vers le fichier .qgz ou .qgs
    :param output_path: Chemin de sortie pour le GeoTIFF
    :param extent: Emprise sous forme de tuple (xmin, ymin, xmax, ymax)
    :param dpi: Résolution en DPI (par défaut 96)
    """
    # Initialiser QGIS (nécessaire pour les scripts autonomes)
    qgs = QgsApplication([], False)
    qgs.initQgis()

    try:
        # Charger le projet
        project = QgsProject.instance()
        project.read(project_path)

        # Configurer les paramètres de la carte
        print(project.crs())
        map_settings = QgsMapSettings()
        map_settings.setLayers(project.mapLayers().values())
        map_settings.setDestinationCrs(project.crs())
        map_settings.setExtent(QgsRectangle(*extent))

        #map_settings.setOutputSize(QSize(800, 600))  # Taille de sortie en pixels

        # Créer un rendu de la carte
        job = QgsMapRendererParallelJob(map_settings)
        job.start()
        job.waitForFinished()

        # Sauvegarder le rendu en GeoTIFF
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

    except Exception as e:
        print(f"Erreur lors de l'export : {e}")

    finally:
        # Désinitialiser QGIS
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
extent = (3700000, 2700000, 3850000, 2800000)
export_map_to_geotiff("src/project.qgz", "tmp/aaa.tiff", extent)



#
qgs.exitQgis()
