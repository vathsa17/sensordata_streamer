# gStreamer with ROS
A ROS Node for streaming image topics from ROS with gStreamer. Using CV2 Bridge for ROS, we stream the image topics with CV2 gStreamer pipeline.


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
