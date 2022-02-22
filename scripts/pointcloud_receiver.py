#############################
# UDP Video Stream Receiver
# A Simple example of Video Stream Receiveing with OpenCV and gStreamer
# Shrivathsa.udupa@gmail.com
#############################

#!/usr/bin/env python
# 

import cv2
import numpy as np
import datetime
import os
import rospy
import open3d as o3d

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("127.0.0.1", 20001))
sock.listen(5)
(client, addr) = sock.accept()


cameraID=62
savePath="/home/in2lab/Data/{}/{}".format(datetime.datetime.now().date(),cameraID)

if not os.path.exists(savePath):
        os.makedirs(savePath)

while True:
        fileSizeAndName = client.recv(128)
        if(fileSizeAndName):
                print("Received a connection from ", addr)
                fileSize = int(fileSizeAndName[:HEADERSIZE])
                client.sendall(bytes("Header received", "utf-8"))
                bSize = 0
                print("Received a connection from ", addr)
                #received_bytes = bytearray(client.recv(2048))
                while True:
                        numpyArBytes=numpyArBytes+client.recv(64000)
                        bSize += 32000
                        if bSize > fileSize:
                                numpyAr=pickle.loads(numpyArBytes)
                                pcd = o3d.geometry.PointCloud()
                                pcd.points = o3d.utility.Vector3dVector(numpyAr)
                                current_date_and_time = datetime.datetime.now()
                                current_date_and_time_string = re.sub(r"[^a-zA-Z0-9]","",str(current_date_and_time))
                                fimename=savePath+"/"+current_date_and_time_string+".ply"
                                o3d.io.write_point_cloud(filename, pcd)
                                print(datetime.datetime.now())
                                break
