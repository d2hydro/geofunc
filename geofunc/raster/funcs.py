# -*- coding: utf-8 -*-

__title__ = 'clump'
__version__ = '0.0.1'
__author__ = 'Daniel Tollenaar'
__license__ = 'MIT'

import numpy as np
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
import logging
 
def clump(data):
    '''Contiguous groups of cells with the same value (‘clumps’)'
    
    Parameters
    ----------
    data: Numpy array with no-data cells as nan (np.NaN).
    
    returns
    ----------
    Numpy array with the data for which clumps are to be returned
    '''

    if not np.isnan(np.sum(data)):
        logging.warning("convert no-data cells to np.NaN before using clump. If not, no-data cells will be clumped too")

    #data = data * 0 + 1
    mask = data.copy()
    mask = mask * 0 + 1
    mask[np.isnan(mask)] = 0
    mask = mask.astype(np.bool)
    geoms = [(shape(s),idx) for idx, (s, v) in enumerate(shapes(data.astype(np.int32), mask=mask))]
    
    clumps = rasterio.features.rasterize(geoms,
                                         out_shape=data.shape,
                                         fill=-999)
    
    return np.where(clumps == -999, np.NaN, clumps)