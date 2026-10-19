#!/usr/bin/env python
"""
FVCOM: Using model input from unstructured grid
===============================================
"""

from datetime import timedelta
import urllib.request as urllib_request
import numpy as np
from opendrift.readers import reader_netCDF_CF_unstructured
from opendrift.readers import reader_global_landmask
# from opendrift.models.oceandrift import OceanDrift
from opendrift.models.sedimentdrift import OceanDrift

o = OceanDrift(loglevel=20)  # Set loglevel to 0 for debug information

try:
    proj = "+proj=utm +zone=9 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    fvcom = reader_netCDF_CF_unstructured.Reader(filename = '/mnt/c/tmp/rpcages03_0001.nc', proj4 = proj)
    o.add_reader(fvcom)
    print(fvcom)
except:
    print('FVCOM output file not available, cannot run example')
    fvcom = None

if fvcom is not None:
    # Seed elements at defined positions, depth and time
    N = 1000
    z = -60.0 #-80*np.random.uniform(0.4, 1, N)
    lat, lon = 49.256676, -125.841559
    o.set_config('drift:vertical_advection', True)
    o.seed_elements(lon=lon, lat=lat, radius=1, number=N,
                    z=z, time=[fvcom.start_time , fvcom.start_time + timedelta(hours=12)],
                    terminal_velocity=0.001)
    #%%
    # Running model
    o.run(time_step=2, time_step_output=300, duration=timedelta(hours=12), outfile='/mnt/c/tmp/rpcages_traj_with_vertical_advection_1day_buoyant.nc')

    #%%
    # Print and plot results
    print(o)
    # o.write_geotiff('/mnt/c/tmp/rpcages.geotiff')
    # o.write_netcdf_density_map(filename='/mnt/c/tmp/rpcages_density.nc')
    #%%
    # Animation (current as background not yet working).
    # o.animation(color='z')

    # o.plot(fast=True, buffer = 1.)

#%%
# .. image:: /gallery/animations/example_fvcom_0.gif

