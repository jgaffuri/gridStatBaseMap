# Initialisation de QGIS
from init_qgis import qgs, QgsUnitTypes, QgsLayoutPoint, QgsLayoutSize, QgsLayoutExporter, QgsLayoutItemMap, QgsPrintLayout, QgsApplication, QgsProject, QgsMapSettings, QgsMapRendererParallelJob, QgsRasterFileWriter, QgsRectangle, QSize
import sys

def export_map(project_path, output_path, extent, scale):
    qgs = QgsApplication([], False)
    qgs.initQgis()
    try:
        project = QgsProject.instance()
        print("Loading project...")
        project.read(project_path)
        #if not project.isValid(): raise ValueError("Project is not valid")

        layout = QgsPrintLayout(project)
        layout.initializeDefaults()
        pc = layout.pageCollection()
        #pc.pages()[0].setPageSize('A4', QgsLayoutSize(QgsLayoutSize.Landscape))
        pc.pages()[0].setPageSize('A4', QgsLayoutSize(width=100,height=100))

        map = QgsLayoutItemMap(layout)
        map.setExtent(QgsRectangle(*extent))
        map.setScale(scale)
        map.attemptMove(QgsLayoutPoint(10, 10, QgsUnitTypes.LayoutMillimeters))
        map.attemptResize(QgsLayoutSize(280, 180, QgsUnitTypes.LayoutMillimeters))
        layout.addLayoutItem(map)

        settings = QgsLayoutExporter.ImageExportSettings()
        settings.dpi = 300

        print("Exporting...")
        exporter = QgsLayoutExporter(layout)
        exporter.exportToImage(output_path, settings)
        print(f"Export terminé : {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        qgs.exitQgis()

'''
scales = []
sca = 102400000
for i in range(5): #13
    scales.append(sca)
    sca /= 2

print(scales)
'''

extent = (3700000, 2700000, 3710000, 2710000)
scale = 1000000
proj = "/home/juju/Bureau/az.qgz"
#proj = "src/project.qgz"
export_map(proj, "tmp/aaa.png", extent, scale)



#
qgs.exitQgis()
