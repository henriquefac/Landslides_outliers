from osgeo import gdal, osr
import numpy as np

class Handler():
    def __init__(self, path):
        self.dataset = gdal.Open(path)
    
    def get_matrix(self, band=1) -> np.ndarray:
        """
        Return a NumPy matrix of the given band. Default is band 1.
        """
        if band < 1 or band > self.dataset.RasterCount:
            raise ValueError(f"Invalid band number: {band}. File has {self.dataset.RasterCount} bands.")
        
        return self.dataset.GetRasterBand(band).ReadAsArray()
    
    