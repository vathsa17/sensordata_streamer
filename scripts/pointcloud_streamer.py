#!/usr/bin/env python

from ipaddress import ip_address
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

HEADERSIZE = 10
topic_name=rospy.get_param('lidar_topic',"/bf_lidar/pointcloud2")
server_address=rospy.get_param('server_ip',"127.0.0.1")
server_port=rospy.get_param('server_port',"20001")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 20002))



def streamer():
    rospy.init_node('pointcloudstreamer', anonymous=True)
    rospy.Subscriber(topic_name, PointCloud2, send)
    rospy.spin()


def send(data):
    pc = ros_numpy.numpify(data)
    numpyArBytes=pickle.dumps(pc, protocol=0)
    contents = bz2.compress(numpyArBytes,compresslevel=9)
    new_msg=True
    print(len(pc))
    print(len(contents))
    msg ="{:<10}".format(str(len(contents)))
    print("Streaming")
    s.sendall(bytes(msg))
    data = s.recv(128)
    print(str(data))
    if(data):
        s.sendall(contents)


if __name__ == '__main__':
    streamer()
