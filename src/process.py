import subprocess


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


def generate_tiles(tiff, output_tiles_dir):
    cmd = [
        "gdal2tiles.py",
        "-p", "EUR",
        "--xyz",
        "--zoom=0-10",
        "-x",
        "-s", "EPSG:3035",
        "--processes=4",
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



qgz_path = "/home/juju/Bureau/map.qgz"
output_tif = "/home/juju/Bureau/gisco/map_background/exported_map.tif"
output_tiles_dir = "/home/juju/Bureau/aaa/"
extent = "2000000,1000000,7000000,5000000 [EPSG:3035]"

export_map_qgis_to_geotiff(qgz_path, output_tif, extent, 8000, 6000, 300)
generate_tiles(output_tif, output_tiles_dir)

