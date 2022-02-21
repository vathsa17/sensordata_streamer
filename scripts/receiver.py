#############################
# UDP Video Stream Receiver
# A Simple example of Video Stream Receiveing with OpenCV and gStreamer
# Shrivathsa.udupa@gmail.com
#############################
import cv2
import numpy as np
cap_receive = cv2.VideoCapture("udpsrc port=5000 ! tsparse ! tsdemux ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false",cv2.CAP_GSTREAMER)
import datetime
from pathlib import Path

cameraID=62
savePath="/home/in2lab/Data/{}/{}".format(datetime.datetime.now().date(),cameraID)

Path("savePath").mkdir(parents=True, exist_ok=True)


writer = None
(h, w) = (480, 640)
zeros = None
write_videos=False
display_frames=True
save_frames=True

if not cap_receive.isOpened():
        print('VideoCapture not opened')
        exit(0)
timeArray=[]

while True:
        
        ret,frame = cap_receive.read()
        e1=cv2.getTickCount()
        if not ret:
                print('empty frame')
                break
        if not writer and write_videos:
                h, w, channels = frame.shape
                fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
                writer = cv2.VideoWriter("received_video.mp4", fourcc, 15,(w , h ), True)
                
        
        #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        if write_videos:
                writer.write(frame)
        if display_frames:
                cv2.imshow('Receive', frame)
        if save_frames:
                current_date_and_time = datetime.datetime.now()
                current_date_and_time_string = re.sub(r"[^a-zA-Z0-9]","",str(current_date_and_time))
                fimename=savePath+"/"+current_date_and_time_string+".jpg"
                cv2.imwrite(fimename,frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
                break
        
