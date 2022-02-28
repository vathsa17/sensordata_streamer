#!/usr/bin/env python

#############################
# Synchronized Image Frame Receiver
# Python script used to receive the compressed image frame from application pc and decomress it and store it as cv2 images
# Shrivathsa.udupa@gmail.com
#############################


 
import re
import bz2
import cv2
import numpy as np
import datetime
import os
import rospy
import socket
import pickle
import struct





numpyArBytes=b''
HEADERSIZE=10
cameraID=62
data_save_path=rospy.get_param('save_path',"/home/in2lab/Data/")
server_IP=rospy.get_param('server_IP',"192.168.199.199")
image_port=rospy.get_param('image_port',"20062")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((server_IP, image_port))


sock.listen(5)
(client_i, addr) = sock.accept()
print("Received a connection from ", addr)


savePath=data_save_path+"/{}/{}".format(datetime.datetime.now().date(),"Image")

print(savePath)
if not os.path.exists(savePath):
        os.makedirs(savePath)




print("Here")
while True:
        fileSizeAndName = client_i.recv(128)
        #print("Receiveing Header")
        if(fileSizeAndName):
            #try:
            fileSize = int(fileSizeAndName[:HEADERSIZE])
            print(fileSize)
            client_i.sendall(bytes("Header received"))
            bSize = 0
            while True:
                    numpyArBytes=numpyArBytes+client_i.recv(64000)
                    print("Receiving Image")
                    bSize += 64000
                    print(len(numpyArBytes))
                    if len(numpyArBytes) == fileSize:
                        try:
                                byte_data=bz2.decompress(numpyArBytes)
                                pc=pickle.loads(byte_data)
                                print(pc.shape)
                                current_date_and_time = datetime.datetime.now()
                                current_date_and_time_string = re.sub(r"[^a-zA-Z0-9]","",str(current_date_and_time))
                                fimename_image=savePath+"/"+current_date_and_time_string+".jpg"
                                cv2.imwrite(fimename_image,pc)
                                print("Saved Image")
                                pc=b''
                                numpyArBytes=b''
                                break
                        except Exception as e:
                                print("Passing")
                                pc=b''
                                numpyArBytes=b''
                                break
        #except Exception as e:
        #    pass
