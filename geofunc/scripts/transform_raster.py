# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:53:06 2020

@author: danie
"""

from geofunc import raster

#%% file paths
clone_raster = r'd:\projecten\H1279.CORIOGLANA20\01.DEM\data\hydrodem_sobek_5m.asc'
source_raster = r'd:\projecten\H1279.CORIOGLANA20\01.DEM\data\glb_dem_26a02_clip_ontwerp_v10.asc'
destination_raster = 'test.asc'

#%% set clone
raster.clone.set_clone(clone_raster, crs = 'epsg:28992')

#%% read input raster
data = raster.read(source_raster, crs = 'epsg:28992')

#%% write output raster
raster.write(data, destination_raster)