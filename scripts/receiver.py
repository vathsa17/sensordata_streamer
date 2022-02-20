#############################
# UDP Video Stream Receiver
# A Simple example of Video Stream Receiveing with OpenCV and gStreamer
# Shrivathsa.udupa@gmail.com
#############################
import cv2
import numpy as np
cap_receive = cv2.VideoCapture("udpsrc port=5000 ! tsparse ! tsdemux ! h264parse ! avdec_h264 ! videoconvert ! appsink sync=false",cv2.CAP_GSTREAMER)

writer = None
(h, w) = (480, 640)
zeros = None
#cv2.namedWindow("receive",cv2.WINDOW_KEEPRATIO)

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
        if not writer:
                h, w, channels = frame.shape
                fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
                writer = cv2.VideoWriter("received_video.mp4", fourcc, 15,(w , h ), True)
                
        
        #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        writer.write(frame)
        
        cv2.imshow('Receive', frame)
        e2=cv2.getTickCount()
        #cv2.resizeWindow("receive",484,304)
        if cv2.waitKey(1)&0xFF == ord('q'):
                break
        
        timeArray.append((e2-e1)/cv2.getTickFrequency())


print("Average processing time per frame is : %5.6f Seconds" %np.nanmean(timeArray))
