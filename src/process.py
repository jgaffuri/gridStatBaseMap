import subprocess
import os

# Chemins des fichiers
qgz_path = "/home/juju/Bureau/map.qgz"
output_tif = "/home/juju/Bureau/gisco/map_background/exported_map.tif"
output_tiles_dir = "/home/juju/Bureau/aaa/"

# Étendue géographique (à adapter selon ton projet)
extent = "2000000,1000000,7000000,5000000 [EPSG:3035]"

# Paramètres d'export
width = 8000
height = 6000
dpi = 300

# 1. Exporter la carte depuis QGIS en GeoTIFF
def export_map_from_qgis():
    cmd = [
        "qgis_process", "run", "native:exportmap",
        "--input=" + qgz_path,
        "--output=" + output_tif,
        "--extent=" + extent,
        f"--width={width}",
        f"--height={height}",
        f"--dpi={dpi}"
    ]
    print("Export de la carte depuis QGIS...")
    try:
        subprocess.run(cmd, check=True)
        print("Export terminé avec succès !")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'export : {e}")
        exit(1)

# 2. Générer les tuiles avec gdal2tiles.py
def generate_tiles():
    cmd = [
        "gdal2tiles.py",
        "-p", "EUR",
        "--xyz",
        "--zoom=0-10",
        "-x",
        "-s", "EPSG:3035",
        "--processes=4",
        output_tif,
        output_tiles_dir
    ]
    print("Génération des tuiles...")
    try:
        subprocess.run(cmd, check=True)
        print("Tuiles générées avec succès !")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la génération des tuiles : {e}")
        exit(1)

# Vérifier que les chemins existent
if not os.path.exists(qgz_path):
    print(f"Erreur : Le fichier {qgz_path} n'existe pas.")
    exit(1)

if not os.path.exists(os.path.dirname(output_tif)):
    print(f"Erreur : Le dossier {os.path.dirname(output_tif)} n'existe pas.")
    exit(1)

# Lancer les étapes
export_map_from_qgis()
generate_tiles()
