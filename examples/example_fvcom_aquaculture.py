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
from opendrift.models.sedimentdrift import SedimentDrift

o = SedimentDrift(loglevel=20)  # Set loglevel to 0 for debug information

try:
    proj = "+proj=utm +zone=9 +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
    fvcom = reader_netCDF_CF_unstructured.Reader(filename = '/mnt/c/tmp/rpcages03_0001.nc', proj4 = proj)
    o.add_reader(fvcom)
    print(fvcom)
except:
    print('FVCOM output file not available, cannot run example')
    fvcom = None

if fvcom is not None:
    # Seed elements at defined positions, depth and time; vertical_mixing:timestep
    settling_velocity= -0.005
    resuspension_threshold = .1
    N = 2000
    z = -20.0 
    lat, lon = 49.256676, -125.841559
    o.set_config('drift:vertical_advection', True)
    o.set_config('drift:vertical_mixing', True)
    o.set_config('vertical_mixing:timestep', 2.0)
    o.set_config('drift:current_uncertainty', 0.05)
    o.set_config('environment:fallback:sea_floor_depth_below_sea_level', 50)
    o.set_config('drift:vertical_advection_correction', True)
    o.set_config('vertical_mixing:resuspension_threshold', resuspension_threshold)
    # o.set_config('general:seafloor_action', 'deactivate')
    fnc = '/mnt/c/tmp/rpcages_traj_sedcore_SSp5_RW5_RS10.nc'


    o.seed_elements(lon=lon, lat=lat, radius=5, number=N,
                    z=z, time=[fvcom.start_time +timedelta(days=5), fvcom.start_time +timedelta(days=5) + timedelta(hours=24)],
                    terminal_velocity=settling_velocity)
    # Running model
    o.run(time_step=2, time_step_output=300, duration=timedelta(hours=24), 
          outfile=fnc)

    # Print and plot results
    print(o)
    # o.write_netcdf_density_map(filename='/mnt/c/tmp/rpcages_density.nc')
    # Animation (current as background not yet working).
    # o.animation(color='z')
    # o.plot(fast=True, buffer = 1.)
# .. image:: /gallery/animations/example_fvcom_0.gif

