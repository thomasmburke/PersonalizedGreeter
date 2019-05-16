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
