import open3d as o3d 
import numpy as np  
import os
import glob
import pcl

files=glob.glob("*.npz")

for f in files:
    numpyAr=np.load(f)
    pc=numpyAr["arr_0"]
    points=np.zeros((pc.shape[0],3))
    points[:,0]=pc['x']
    points[:,1]=pc['y']
    points[:,2]=pc['z']
    p = pcl.PointCloud(np.array(points, dtype=np.float32))
    filename=f[:-4]+".pcd"
    pcl.save(p,filename)

files=glob.glob("*.pcd")
pcd = o3d.io.read_point_cloud(files[0])
o3d.visualization.draw_geometries([pcd])
