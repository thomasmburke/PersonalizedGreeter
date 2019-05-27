# When using a virtualenv I encountered issues importing the following python
# libraries without the dependecies found below

# before pyaudio
sudo apt-get install portaudio19-dev
# before pygame
sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev


# Setup to get usb speaker to work on card 1 of raspberry pi
sudo vi /etc/asound.conf
#then add the following code:
pcm.!default  {
 type hw card 1
}
ctl.!default {
 type hw card 1
}


# Installing OpenCV on Raspberry Pi
# start by clearing 700MB of space
sudo apt-get purge wolfram-engine
# update and upgrade existing packages
sudo apt-get update
sudo apt-get upgrade
# install some developer tools i.e. cmake to configure OPENCV build process
sudo apt-get install build-essential cmake pkg-config
# install some image I/O packages
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
# Install video I/O packages
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev
# Install to handle OPENCV highgui
sudo apt-get install libgtk2.0-dev
# optimize OPENCV's matrix operations with these dependecies
sudo apt-get install libatlas-base-dev gfortran
# Install python header files
sudo apt-get install python2.7-dev python3-dev
# Download OPENCV source code
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
unzip opencv_contrib.zip
# in a virtual env you should have numpy installed
pip3 install numpy
# Compile and install OPENCV
cd ~/opencv-3.1.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D ENABLE_PRECOMPILED_HEADERS=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
    -D BUILD_EXAMPLES=ON ..
# Compile OPENCV with all 4 cores
make -j4
# if the make -j4 fails it is due to race conditions in which case you should run
make clean
make # this will use only one core
# Install OPENCV on the raspberry pi
sudo make install
sudo ldconfig
# Verify your OPENCV bindings are in the correct location
ls -l /usr/local/lib/python3.5/site-packages/
"""
I honestly don’t know why, perhaps it’s a bug in the CMake script, but when compiling OpenCV 3 bindings for Python 3+, the output .so  file is named cv2.cpython-34m.so  (or some variant of) rather than simply cv2.so  (like in the Python 2.7 bindings).

Again, I’m not sure exactly why this happens, but it’s an easy fix. All we need to do is rename the file:
"""
cd /usr/local/lib/python3.5/site-packages/
sudo mv cv2.cpython-35m.so cv2.so
# symlink our opencv bindings to the virtualenv
cd ~/Desktop/envs/PersonalizedGreeter/lib/python3.5/site-packages/
ln -s /usr/local/lib/python3.4/site-packages/cv2.so cv2.so
# Remove directories to free up disk space
rm -rf ~/opencv-3.1.0 ~/opencv_contrib-3.1.0
