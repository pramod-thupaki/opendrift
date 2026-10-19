import numpy as np
import OM.modelling_toolbox.fvcom_toolbox as fvt
# from OM.mesh_utils import meshUtils
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import cmocean.cm as cmap
import xarray as xr 
from pyproj import Proj, Transformer

# Define source and target coordinate systems
wgs84 = Proj(proj="latlong", datum="WGS84") # Source CRS (latitude/longitude)
UTM9N = Proj(proj="utm", zone=9, datum="WGS84") # Target CRS (UTM Zone 31N)

# Using Transformer for modern pyproj versions
utm2wgs = Transformer.from_proj(UTM9N, wgs84, always_xy=True)
wgs2utm = Transformer.from_proj(wgs84, UTM9N, always_xy=True)
fnc = 'rpcages_traj_sedcore_SSp1_RW5_RS100.nc'
df = xr.open_dataset(f'/mnt/c/tmp/{fnc}')
nv, ndxy = fvt.readMesh_V3("/mnt//c/projects/csrf2025/rpcages_input_files/rp02_grd.dat")

lon, lat = utm2wgs.transform(ndxy[:,0], ndxy[:,1]) 
trimesh = mtri.Triangulation(ndxy[:,0], ndxy[:,1], nv - 1)

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(8,10), sharex=True)

# plot only particles that are moving in black and those settled as red
ax = axs[0]
for i in range(df.lon.shape[0]):
    x, y = wgs2utm.transform(df.lon[i,:], df.lat[i,:])
    ax.scatter(x, y, c='b', alpha=0.1)

ax.triplot(trimesh, lw=0.1, c="k")
ax.axis("equal")
x0, y0 = wgs2utm.transform(np.mean(df.lon[:,0]), np.mean(df.lat[:,0]))
dx, dy = 500,400
print(x0, y0)
ax.set_xlim([x0-dx, x0+dy])
ax.set_ylim([y0-dy, y0+dy])
# print(df)
# =============================================================================
# plot initial and final locations
ax = axs[1]
# final
x, y = wgs2utm.transform(df.lon[:,-1], df.lat[:,-1])
id_moving = np.argwhere(df.moving[:,-1].values==1)
id_settled = np.argwhere(df.moving[:,-1].values==0)
id_nan = np.argwhere(np.isnan(df.moving[:,-1].values))
print(f'nan {len(id_nan)}, moving {len(id_moving)}, settled {len(id_settled)}')
ax.scatter(x[id_settled], y[id_settled], c='b', alpha=0.2)
# ax.scatter(x[id_nan], y[id_nan], c='r', alpha=0.2)
m = ax.scatter(x[id_moving], y[id_moving], c=df.z[:,-1].values[id_moving],cmap='magma', alpha=.2)
cax = fig.add_axes([0.92, 0.2, 0.02, 0.2])  
plt.colorbar(cax=cax, mappable=m)
# initial
x, y = wgs2utm.transform(df.lon[:,0], df.lat[:,0])
ax.scatter(x, y, c='r')

ax.triplot(trimesh, lw=0.1, c="k")
ax.axis("equal")
ax.set_xlim([x0-dx, x0+dx])
ax.set_ylim([y0-dy, y0+dy])
fpng = fnc.split('.')[0]+'.png'
print(fpng)
plt.savefig(f'/mnt/c/tmp/figs/{fpng}')


