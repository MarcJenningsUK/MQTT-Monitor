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

## What's it doing?
The Python script is there to run in a loop, listening to events coming from the MQTT server.  When it recieves those events, it stores the data in local variables and writes out an image file (3 files actually, but we'll come to that)
There's a shell script that gets called to open [fbi](https://packages.debian.org/sid/fbi) which will loop through the image files and output them directly to the framebuffer.  Fbi will work with fewer than three images, but there's a small gotcha in that you can't reliably disable image caching for fewer than three.  If we write out three images and loop through them, then the 
``` --cachemem 0 ```
argument becomes effective and images are reloaded from disk each time.

## Running it
I know there's a better way, and certainly a more secure one, but since my device is running in my home without an attached keyboard I just set the Pi to boot directly to the console logged in as the default user (pi).  In ```/home/pi/.bashrc``` I added a call to the Python script.  That's it.

## What's next?
I am looking at options to accept touch input from the display (I'm using a Pimoroni [HyperPixel](https://shop.pimoroni.com/products/hyperpixel) display which includes touch support.  When I get some time I'll try to hook into the event for that to control what gets written to the files.  That *should* let me allow the user (me) to cycle through different information via touch.
