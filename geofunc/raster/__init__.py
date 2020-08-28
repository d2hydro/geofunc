import logging
import numpy as np
from pathlib import Path
import rasterio
from rasterio.warp import reproject, Resampling
import sys


class Clone:
    
    def __init__(self, profile=None, scales=None, overviews=None, crs=None):
        self.profile = profile
        self.scales = scales
        self.overviews = overviews
        self.crs = crs
        
    
    def set_clone(self, raster_file, crs=None):
        raster_file = Path(raster_file)
        if raster_file.exists():
            with rasterio.open(raster_file) as src:
                self.profile = src.profile
                self.scales = src.scales
                self.overview = src.overviews
        
        if crs:
            self.profile['crs'] = crs
        if not self.profile['crs']:
            logging.warning('crs not provided, please specify Clone.crs before saving rasters')

        
        if self.profile['driver'] == 'AAIGrid':
            self.profile.pop('tiled', None)
        
        else:
            logging.warning(f'{raster_file} does not exist')
                
clone = Clone()

def __change_carrier_return(asc_file):
    
    asc_file = Path(asc_file)
    data = asc_file.read_bytes()
    data = data.replace(b'\n', b'\r\n')
    asc_file.write_bytes(data)

def read(raster_file, resampling = Resampling.nearest, crs = None):
    '''function to read a raster to numpy array'''
    
    if clone.profile['crs']:
        dst_crs = clone.profile['crs']
    elif clone.crs:
        dst_crs = clone.crs
    else:
        logging.error('provide crs for clone first')
        sys.exit()
    
    raster_file = Path(raster_file)
    if raster_file.exists():
        with rasterio.open(raster_file) as src:
            src_transform = src.profile['transform']
            if crs:
                src_crs = crs
            elif src.profile['crs']:
                src_crs = src.profile['crs']
            else:
                logging.error('raster_file does not contain crs. Please provide one in function-variable')
                sys.exit()
            src_data = src.read(1)
            src_data = np.where(src_data == src.profile['nodata'], np.NaN, src_data)
            src_data = src_data * src.scales[0]
            
        dst_data = np.empty((clone.profile['height'], (clone.profile['width'])))
        reproject(source = src_data,
                  destination = dst_data,
                  src_transform = src_transform,
                  src_crs = src_crs,
                  dst_transform = clone.profile['transform'],
                  dst_crs = dst_crs,
                  resampling = resampling,
                  src_nodata = np.NaN,
                  dst_nodata = np.NaN
                  )
        return dst_data
    
    else:
        logging.warning(f'raster_file {raster_file} does not exist')

def write(data, raster_file):
    '''function to write a raster to file'''
    
    if not clone.profile == None:
        profile = clone.profile
        if not clone.scales == None:
            data = data * clone.scales
        
        if not profile['crs']:
            if clone.crs:
                profile['crs'] = clone.crs
                
        data = np.where(np.isnan(data), profile['nodata'], data)
        data = data.astype(np.dtype(profile['dtype']))
        
        raster_file = Path(raster_file)
        if raster_file.exists():
            raster_file.unlink()
        else:
            raster_file.parent.mkdir(parents=True, exist_ok=True)
        with rasterio.open(raster_file, 'w', **profile) as dst:
            dst.write(data,1)
            if clone.scales:
                dst.scales = clone.scales
            dst.overview = clone.overviews    
            
        if profile['driver'] == 'AAIGrid':
            __change_carrier_return(raster_file)
            
    else:
        logging.warning(r'set clone by raster.clone.set_clone(raster_file). Or specify rater.clone.profile with a rasterio profile')
        
        

        