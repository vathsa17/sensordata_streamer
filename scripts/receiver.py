#!/usr/bin/env python
#############################
# UDP Video Stream Receiver
# A Simple example of Video Stream Receiveing with OpenCV and gStreamer
# Shrivathsa.udupa@gmail.com
#############################




import cv2
import numpy as np
import datetime
import os
import rospy
import re
import socket
import pickle
import re
import bz2
import redis
import struct

savePath="/home/in2lab/Data/{}/{}/".format(datetime.datetime.now().date(),"Mast_Right")
cap_receive = cv2.VideoCapture("udpsrc port=5000 ! tsparse ! tsdemux ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false",cv2.CAP_GSTREAMER)


print("Stream Receving")

writer = None
(h, w) = (480, 640)
zeros = None
write_videos=False
display_frames=False
save_frames=True

frame=[]

if not cap_receive.isOpened():
        print('VideoCapture not opened')
        exit(0)
timeArray=[]

r = redis.Redis(host='localhost', port=6379, db=0)

def toRedis(r,a,n):
   """Store given Numpy array 'a' in Redis under key 'n'"""
   h, w = a.shape[:2]
   shape = struct.pack('>II',h,w)
   encoded = shape + a.tobytes()

   # Store encoded data in Redis
   r.set(n,encoded)
   return

while True:
        
        ret,frame = cap_receive.read()
        toRedis(r, frame, 'image')
        if not ret:
                print('empty frame')
                break
        #if not writer and write_videos:
        #        h, w, channels = frame.shape
        #        fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        #        writer = cv2.VideoWriter("received_video.mp4", fourcc, 15,(w , h ), True)
                

        #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        """
        if write_videos:
                writer.write(frame)
        if display_frames:
                cv2.imshow('Receive', frame)
                print("Saving")
        if save_frames:
                current_date_and_time = datetime.datetime.now()
                current_date_and_time_string = re.sub(r"[^a-zA-Z0-9]","",str(current_date_and_time))
                fimename_image=savePath+"/"+current_date_and_time_string+".jpg"
                cv2.imwrite(fimename,frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
                break
        """
