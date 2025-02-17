from osgeo import gdal, osr
import rasterio
import geopandas as gpd
from rasterio.mask import mask
import numpy as np
import os


class Handler():
    def __init__(self, path):
        self.path = path
        self.dataset = gdal.Open(path)
    
    # retorna matriz da banda atribuida
    def get_matrix(self, band=1) -> np.ndarray:
        """
        Return a NumPy matrix of the given band. Default is band 1.
        """
        if band < 1 or band > self.dataset.RasterCount:
            raise ValueError(f"Invalid band number: {band}. File has {self.dataset.RasterCount} bands.")
        
        return self.dataset.GetRasterBand(band).ReadAsArray()
    
    # recorta a matriz da banda recortada a partirt de um shapefile
    def cropTiff(self, path_shp):
        shapefile = gpd.read_file(path_shp)
        geometria = [feature.__geo_interface__ for feature in shapefile.geometry]
        
        # abrir arquivo tiff
        with rasterio.open(self.path) as src:
            out_image, out_transform = mask(src, geometria, crop=True)
            
            # metadados
            out_meta = src.meta.copy()
        
        return (out_image[0], out_transform, out_meta)
    
    def getCrop(self, path_shp):
        return self.cropTiff(path_shp)[0]
    
    def saveCrop(self, path_shp, name=None, path_crop_dir=None):
        if not path_crop_dir:
            # get dir from original path
            path_crop_dir = os.path.dirname(self.path)
        if not name:
            name = os.path.basename(self.path).split(".")[0] + "_crop.tif"

        path_crop = os.path.join(path_crop_dir, name)

        out_image, out_transform, out_meta = self.cropTiff(path_shp)

        out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
        })

        with rasterio.open(path_crop, "w", **out_meta) as dest:
            dest.write(out_image)
