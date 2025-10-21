import subprocess

/home/juju/workspace/gridStatBaseMap/src/project.qgz
'''
qgis_process run native:exportmap \
  --input="/home/juju/workspace/gridStatBaseMap/src/project.qgz" \
  --output="/home/juju/Bureau/exported_map.tif" \
  --extent="3700000,2700000,3710000,2710000 [EPSG:3035]" \
  --width=5000 \
  --height=5000 \
  --dpi=300
'''

def export_map_qgis_to_geotiff(qgz_path, output_tif, extent, width, height, dpi):
    cmd = [
        "qgis_process", "run", "native:exportmap",
        "--input=" + qgz_path,
        "--output=" + output_tif,
        "--extent=" + extent,
        f"--width={width}",
        f"--height={height}",
        f"--dpi={dpi}"
    ]
    print("Export map from QGIS...")
    try:
        subprocess.run(cmd, check=True)
        print("Export terminé avec succès !")
    except subprocess.CalledProcessError as e:
        print(f"Map export error: {e}")
        exit(1)


def generate_tiles(tiff, output_tiles_dir, zmin=0, zmax=10, profile = "EUR", crs = "EPSG:3035", processes=4):
    cmd = [
        "gdal2tiles.py",
        "-p", profile,
        "--xyz",
        "--zoom="+str(zmin)+"-"+str(zmax),
        "-x",
        "-s", crs,
        "--processes="+str(processes),
        tiff,
        output_tiles_dir
    ]
    print("Tiling...")
    try:
        subprocess.run(cmd, check=True)
        print("Tiling done.")
    except subprocess.CalledProcessError as e:
        print(f"Error while tiling: {e}")
        exit(1)



#qgz_path = "src/project.qgz"
qgz_path = "/home/juju/Bureau/az.qgz"
output_tif = "tmp/exported_map.tif"
output_tiles_dir = "tmp/tiles/"
extent = "3700000,2700000,3710000,2710000 [EPSG:3035]"

export_map_qgis_to_geotiff(qgz_path, output_tif, extent, 8000, 6000, 300)
#generate_tiles(output_tif, output_tiles_dir)

