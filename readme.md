# Sensor Data Streamer from ROS master to Remote server
A ROS Node for streaming image topics and pointcloud from ROS with gStreamer and UDP sockets. At he receiving end you you can store the images and pointclouds synchronously. Using CV2 Bridge for ROS, we stream the image topics with CV2 gStreamer pipeline. We use UDP sockets to stream the received pointcloud. 

![alt text](images/Setup.PNG)

## For Camera Images
At sensor end, we subscribe to image topics. The ROS image topics are first converted to CV2 images using cv2_bridge. You can subscribe to raw image or compressed image. Configuration parameters can be edited in launch file.

At the receiver end, gStreamer pipeline will receive the video frame into CV2 environment. We then use redis to store the image frame temporarily in the local PC.

## For Lidar Point Clouds
At Streamer end, we subscribe to "Pointcloud2" topic and data from the topic will be first converted to numpy array, pickeled it to serialize the data and compressed using bz2.  

At the receiveing end, the data will be received from UDP sockets and first unzip and depickled and then stored as compressed numpy array. With postprocessing, we can convert the npz array into .pcd file.

For every pointcloud received, we check the latest image frame from the redis server and write this image into the storage path.

The code primarily developed to record the sensor data in the R&D Project IN2Lab.


**LAYOUT:**
- gStreamer_ROS/
  - launch/:              roslaunch files
  - src/:                 source files
  - script/:			Python scripts for the project
  - CMakeLists.txt:       CMake project configuration file
  - package.xml:          ROS/Catkin package file

**REQUIREMENTS:**

CV2 built from source with gStreamer package is required to write CV2 pipeline for gStreamer.

**SETUP:**

Clone the repository into your catkin workspace and build with catkin_make

**LAUNCH:**

A Sample launch script is provided in the launch directory. Configure the topic names and other parameters here
