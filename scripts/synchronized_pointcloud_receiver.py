#!/usr/bin/env python

#!/usr/bin/env python

#############################
# Synchronized Pointcloud Receiver
# Python script for receiveing Synchronized Pointclouds from Sensor Application PC
# Shrivathsa.udupa@gmail.com
#############################


 
import re
import bz2
import cv2
import numpy as np
import datetime
import os
import rospy
#import open3d as o3d
import socket
import pickle
#import pcl
import struct


numpyArBytes=b''
HEADERSIZE=10
data_save_path=rospy.get_param('save_path',"/home/in2lab/Data/")
server_IP=rospy.get_param('server_IP',"192.168.199.199")
pointcloud_port=rospy.get_param('pointcloud_port',"20067")
savePath=data_save_path+"/{}/{}".format(datetime.datetime.now().date(),"Lidar")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server_IP, pointcloud_port))
sock.listen(5)
(client, addr) = sock.accept()
print("Received a connection from ", addr)

print(savePath)
if not os.path.exists(savePath):
        os.makedirs(savePath)




print("Here")
while True:
        fileSizeAndName = client.recv(128)
        #print("Receiveing Header PCD")
        if(fileSizeAndName):
            #try:
            fileSize = int(fileSizeAndName[:HEADERSIZE])
            print(fileSize)
            client.sendall(bytes("Header received"))
            bSize = 0
            while True:
                    numpyArBytes=numpyArBytes+client.recv(16000)
                    print("Receiving")
                    bSize += 16000
                    if len(numpyArBytes) == fileSize:
                        #try:
                        byte_data=bz2.decompress(numpyArBytes)
                        pc=pickle.loads(byte_data)
                        print(len(pc))
                        current_date_and_time = datetime.datetime.now()
                        current_date_and_time_string = re.sub(r"[^a-zA-Z0-9]","",str(current_date_and_time))
                        filename=savePath+"/"+current_date_and_time_string+".npz"
                        np.savez_compressed(filename,pc)
                        print("Saved Pointcloud")
                        pc=b''
                        numpyArBytes=b''
                        break
                        #except Exception as e:
                        #    print("Passing")
                        #    pc=b''
                        #    numpyArBytes=b''
                        #    break
        #except Exception as e:
        #    pass