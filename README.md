# MQTT-Monitor
Python script for rPI to display specific detail from MQTT Feeds

I wanted a small, lightweight setup to run on a Pi Zero with a colour display but without the overhead of running full X.  I decided to go down the route of subscribing to a specific topic section in my MQTT broker and using Python / Pillow to render an image.  That image is then displayed by FBI at the command line direct to the frame buffer.

## Pre-requisites
```
sudo apt-get install fbi  
sudo pip install paho-mqtt  
sudo pip install pillow  
```

Running MQTT broker.
