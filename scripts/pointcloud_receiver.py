#!/usr/bin/env python

#############################
# UDP Video Stream Receiver
# A Simple example of Video Stream Receiveing with OpenCV and gStreamer
# Shrivathsa.udupa@gmail.com
#############################


 
import re
import bz2
import cv2
import numpy as np
import datetime
import os
import redis
#import rospy
#import open3d as o3d
import socket
import pickle
#import pcl
import struct

r = redis.Redis(host='localhost', port=6379, db=0)
def fromRedis(r,n):
   """Retrieve Numpy array from Redis key 'n'"""
   encoded = r.get(n)
   h, w = struct.unpack('>II',encoded[:8])
   a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
   return a


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 20002))
sock.listen(5)
(client, addr) = sock.accept()
print("Received a connection from ", addr)

numpyArBytes=b''
HEADERSIZE=10
cameraID=62
savePath="/home/in2lab/Data/{}/{}".format(datetime.datetime.now().date(),"Lidar")

print(savePath)
if not os.path.exists(savePath):
        os.makedirs(savePath)




print("Here")
while True:
        fileSizeAndName = client.recv(128)
        if(fileSizeAndName):
                #print("Received a connection from ", addr)
                fileSize = int(fileSizeAndName[:HEADERSIZE])
                print(fileSize)
                client.sendall(bytes("Header received"))
                bSize = 0
                #print("Received a connection from ", addr)
                #received_bytes = bytearray(client.recv(2048))
                while True:
                        numpyArBytes=numpyArBytes+client.recv(65500)
                        print("HERE")
                        bSize += 65000
                        if bSize > fileSize:
                                #numpyArBytes[:]=numpyArBytes_r
                                #print(len(numpyArBytes))
                                byte_data=bz2.decompress(numpyArBytes)
                                pc=pickle.loads(byte_data)
                                #points=np.zeros((pc.shape[0],3))
                                #points[:,0]=pc['x']
                                #points[:,1]=pc['y']
                                #points[:,2]=pc['z']
                                #p = pcl.PointCloud(np.array(points, dtype=np.float32))
                                print(len(pc))
                                #pcd = o3d.geometry.PointCloud()
                                #print(len(numpyAr))
                                #pcd.points = o3d.utility.Vector3dVector(numpyAr)
                                current_date_and_time = datetime.datetime.now()
                                current_date_and_time_string = re.sub(r"[^a-zA-Z0-9]","",str(current_date_and_time))
                                filename=savePath+"/"+current_date_and_time_string+".npz"
                                img = fromRedis(r,'image')
                                fimename_image=savePath+"/"+current_date_and_time_string+".jpg"
                                cv2.imwrite(fimename_image,img)
                                #o3d.io.write_point_cloud(filename, pcd)
                                #print(datetime.datetime.now())
                                np.savez_compressed(filename,pc)
                                #pcl.save(p,savepath)
                                pc=b''
                                numpyArBytes=b''
                                break
