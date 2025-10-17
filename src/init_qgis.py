import sys
from qgis.core import QgsApplication

# Chemin vers le répertoire d'installation de QGIS
qgis_prefix = "/usr"

# Initialiser QgsApplication
qgs = QgsApplication([], False)
qgs.setPrefixPath(qgis_prefix, True)
qgs.initQgis()

# Importer les modules nécessaires après l'initialisation
from qgis.core import QgsProject, QgsMapSettings, QgsMapRendererParallelJob, QgsRasterFileWriter, QgsRectangle
from qgis.gui import QgsMapCanvas
from PyQt5.QtCore import QSize
