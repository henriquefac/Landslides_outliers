import os
import rasterio
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from rasterio.mask import mask

# Caminhos dos arquivos
base_path = r"/home/henrique/Documents/tif_proj"
raster_dir_path = os.path.join(base_path, "files_raster")
shape_dir_path = os.path.join(base_path, "shape_file")

tif_file_path = os.path.join(raster_dir_path, "gebco_2024_n0.0_s-90.0_w-90.0_e0.0.tif")
crop_tif_file_path = os.path.join(raster_dir_path, "crop.tif")
shape_file_path = os.path.join(shape_dir_path, "CE_Municipios_2022.shp")

from raster_handler.handler import Handler as hd

handler = hd(tif_file_path)


