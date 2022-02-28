# Requirements for the Package
All the requirements are tested and documented for Ubuntu 18.04 environment.

## At Server PC
### Redis server
Install the redis server with 

sudo apt-get install redis-server

Then demonize the redis-server with 
redis-server --daemonize yes

### Install Python PCL
sudo apt install libpcl-dev -y
pip install python-pcl (or pip3)

## At Application PC (Sensor PC)
bz2
