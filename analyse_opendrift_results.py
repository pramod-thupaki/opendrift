import xarray as xr 
import matplotlib.pyplot as plt 

df = xr.open_dataset('/mnt/c/tmp/rpcages_traj_sedcore_SS1_RW5_RS1.nc')
print(df.moving.shape)
print(df.z.shape)
print(df.status.shape)
for i in range(1,1000, 4):
    plt.plot(df.time[:], df.z[i,:])
plt.savefig('tmp.png')