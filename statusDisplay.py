import paho.mqtt.client as mqtt
from PIL import Image, ImageDraw, ImageFont
from subprocess import call

# fbi requires three images to work with in order to force no-cache of the files.  
# Let's initialise three images...
call(["cp", "/home/pi/splash.jpg", "/mnt/ramdisk/status1.jpg"])
call(["cp", "/home/pi/splash.jpg", "/mnt/ramdisk/status2.jpg"])
call(["cp", "/home/pi/splash.jpg", "/mnt/ramdisk/status3.jpg"])

# fbi displays files from the filelist file, which is set up by default to use the images we initialised above.  
# It will rotate through the images every 5 seconds.
# It is possible to add three referencess to the same file, but I wanted to try to minimise the chances of trying to write to an open file.
# We launch it from a shell script because I'm too inexperience to be able to reliably call it from a python script as root and have it function
call(["/bin/bash", "/home/pi/displayImg.sh"])

# set up some global vars to hold historical data
lrtemp = 0
lrhumid = 0
gatemp = 0
gahumid = 0;

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    client.subscribe("ESP8266/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global lrtemp, lrhumid, gatemp, gahumid

    if(msg.topic == "ESP8266/lounge/temperature"):
        lrtemp = msg.payload
    if(msg.topic == "ESP8266/lounge/humidity"):
        lrhumid = msg.payload
    if(msg.topic == "ESP8266/garage/temperature"):
        gatemp = msg.payload
    if(msg.topic == "ESP8266/garage/humidity"):
        gahumid = msg.payload

    # draw the values out to an image variable.  If your display is not 800*480, adjust the initialisation here.  It'll still work with these defaults but fbi will auto-zoom to be able to display the output.
    image = Image.new('RGB',(800,480))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("SegoeWP.ttf",48)
    draw.text((20,50), 'Lounge Temp', font=font, fill=(0,0,255))
    draw.text((20,100), str(lrtemp), font=font, fill=(255,0,0))
    draw.text((20,150), 'Lounge Humidity', font=font, fill=(0,0,255))
    draw.text((20,200), str(lrhumid), font=font, fill=(255,0,0))
    draw.text((20,250), 'Garage Temp', font=font, fill=(0,0,255))
    draw.text((20,300), str(gatemp), font=font, fill=(255,0,0))
    draw.text((20,350), 'Garage Humidity', font=font, fill=(0,0,255))
    draw.text((20,400), str(gahumid), font=font, fill=(255,0,0))
    
    # and then save the image out to the three files.
    image.save("/mnt/ramdisk/status1.jpg")
    image.save("/mnt/ramdisk/status2.jpg")
    image.save("/mnt/ramdisk/status3.jpg")
    

# Set up the connection and events.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.fqdn", 1883, 60)

# loop forever (duh!)
client.loop_forever()
