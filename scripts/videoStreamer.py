#!/usr/bin/env python

from ipaddress import ip_address
import cv2
import sys
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage


bridge = CvBridge()
frames=rospy.get_param('fps',10)
w=rospy.get_param('width',640)
h=rospy.get_param('height',480)
topic_name=rospy.get_param('Camera_image_topic',"/camera/image_raw")
server_address=rospy.get_param('server_ip',"10.147.20.66")
pipeline_info='appsrc is-live=true ! videoconvert ! x264enc tune=zerolatency noise-reduction=1000 speed-preset=superfast byte-stream=true threads=8 key-int-max=15 intra-refresh=true !mpegtsmux ! udpsink host={} port=5000'.format(server_address)
fourcc = cv2.VideoWriter_fourcc(*'H264')
isCompressed=rospy.get_param("isCompressed",True)
# Setting up gStreamer pipeline
out = cv2.VideoWriter(pipeline_info,0,frames, (w,h),True) #ouput GStreamer pipeline
if not out.isOpened():
    print('VideoWriter not opened')
    exit(0)



#print(cv2.getBuildInformation())


def streamer():
    rospy.init_node('videostreamer', anonymous=True)
    if isCompressed:
        rospy.Subscriber(topic_name, CompressedImage, send)
    else:
        rospy.Subscriber(topic_name, Image, send)
    rospy.spin()


def send(data):
    if isCompressed:
        frame=bridge.compressed_imgmsg_to_cv2(data,"bgr8")
    else:
        frame=bridge.imgmsg_to_cv2(data, "bgr8")
    #print("Streaming")
    if(h,w != frame.shape[:2]):
        frame=cv2.resize(frame,(w,h))
    cv2.imshow("Sent",frame)
    out.write(frame)
    if cv2.waitKey(1)&0xFF == ord('q'):
    	sys.exit(0)
    


if __name__ == '__main__':
    streamer()
