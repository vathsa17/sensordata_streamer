#!/usr/bin/env python
import rospy
import message_filters
import socket
from sensor_msgs.msg import CompressedImage, PointCloud2
import sys
import rospy
from sensor_msgs.msg import PointCloud2
import socket
import os
import threading
#import open3d as o3d
import pickle
import numpy as np
import datetime
import ros_numpy
import bz2
import rospy
from cv_bridge import CvBridge
bridge = CvBridge()
from io import StringIO,BytesIO
import cv2
from pb_msgs.msg import ClusterList

b=BytesIO()

def send_radarCluser(radar_data):
    d=radar_data.serialize(buff=b)
    serialized_data=b.getvalue()
    contents = bz2.compress(serialized_data,compresslevel=9)
    msg_p ="{:<10}".format(str(len(contents)))
    print("Streaming Radar Data",msg_p)
    radardata_s.sendall(bytes(msg_p))
    data_p = radardata_s.recv(128)
    print(str(data_p))
    if(data_p):
        radardata_s.sendall(contents)



def send_pointcloud(pcd):
    pc = ros_numpy.numpify(pcd)
    numpyArBytes=pickle.dumps(pc, protocol=0)
    contents = bz2.compress(numpyArBytes,compresslevel=9)
    new_msg=True
    msg_p ="{:<10}".format(str(len(contents)))
    print("Streaming PCD",msg_p)
    pointcloud_s.sendall(bytes(msg_p))
    data_p = pointcloud_s.recv(128)
    print(str(data_p))
    if(data_p):
        pointcloud_s.sendall(contents)

def send_image(img):
    if isCompressed:
        imgd=bridge.compressed_imgmsg_to_cv2(img,"bgr8")
    else:
        imgd=bridge.imgmsg_to_cv2(img, "bgr8")

    if(h,w != imgd.shape[:2]):
        imgd=cv2.resize(imgd,(w,h))
    if not isColor:
        imgd=cv2.cvtColor(imgd, cv2.COLOR_BGR2GRAY)
    numpyArBytes=pickle.dumps(imgd, protocol=0)
    contents = bz2.compress(numpyArBytes,compresslevel=9)
    new_msg=True
    print(len(imgd))
    print(len(contents))
    msg_i ="{:<10}".format(str(len(contents)))
    print("Streaming Image",msg_i)
    image_s.sendall(bytes(msg_i))
    data_i = image_s.recv(128)
    print(str(data_i))
    if(data_i):
        image_s.sendall(contents)


def callback(image, pointcloud,radar_data):
    print("IN CALLBACK")
    send_image(image)
    send_pointcloud(pointcloud)
    send_radarCluser(radar_data)

image_topic_name=rospy.get_param('Camera_image_topic',"/camera/image_raw")
pointcloud_topic_name=rospy.get_param('lidar_topic',"/bf_lidar/pointcloud2")
radardata_topic_name=rospy.get_param('radar_topic',"/RadarFrames")


server_address=rospy.get_param('server_ip',"127.0.0.1")


image_server_port=rospy.get_param('image_server_port',"20063")
pointcloud_server_port=rospy.get_param('pointcloud_server_port',"20067")
radardata_server_port=rospy.get_param('radardata_server_port',"20068")


isCompressed=rospy.get_param("isCompressed",True)
isColor=rospy.get_param("isColor",False)
w=rospy.get_param('width',640)
h=rospy.get_param('height',480)

image_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
image_s.connect((server_address, image_server_port))

pointcloud_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pointcloud_s.connect((server_address, pointcloud_server_port))

radardata_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
radardata_s.connect((server_address, radardata_server_port))

rospy.init_node('datastreamer', anonymous=True)
print("Filtering from",image_topic_name,pointcloud_topic_name,radardata_topic_name)
if isCompressed:
    image_sub = message_filters.Subscriber(image_topic_name, CompressedImage)
else:
    image_sub = message_filters.Subscriber(image_topic_name, Image)

pointcloud_sub = message_filters.Subscriber(pointcloud_topic_name, PointCloud2)

radardata_sub=message_filters.Subscriber(radardata_topic_name, ClusterList)


ts = message_filters.ApproximateTimeSynchronizer([image_sub, pointcloud_sub,radardata_sub], queue_size=50, slop=0.5,allow_headerless=True)
ts.registerCallback(callback)
rospy.spin()