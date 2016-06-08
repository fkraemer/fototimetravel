# -*- coding: utf-8 -*-

#!/usr/bin/env python
import argparse
from datetime import datetime
from itertools import izip
from os import system, path
from PIL import Image, ImageDraw, ImageFont
import random

parser = argparse.ArgumentParser(description='Search in the DB to give back an image from the same day some years ago')
parser.add_argument('file', type=str,
                   help="the file where the fotobase will be read from")

def editPhotoAndCopyToTemp(image,year):
    head, tail = path.split(image)
    newImagefilepath = "/tmp/{}".format(tail)
    #Read image
    im = Image.open(image)
    #manipulate
    draw = ImageDraw.Draw(im)
    fontFile = "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono.ttf"
    font = ImageFont.truetype(fontFile, 100)
    draw.text((im.size[0] - 350, im.size[1] - 400),str(year),(73,72,66),font=font)    
    #save
    
    im.save( newImagefilepath, 'JPEG' )
    return newImagefilepath

def main():
    args = parser.parse_args()
    with open(args.file) as f:
        content = f.readlines()
    filenames = []
    timestamps = []
    for c in content:
        filename, timestamp = c.split(';')
        filenames.append(filename)
        timestamps.append(datetime.fromtimestamp(float(timestamp)))
    print "Read {} pics from {}".format(len(timestamps),args.file)
    today = datetime.now()
    listToChooseFrom = []
    for f,t in izip(filenames, timestamps):
        if t.day == today.day and t.month == today.month:
            print "{} was shot the same day {} years ago".format(f,today.year-t.year)
            listToChooseFrom.append( (f, t.year))
    
    image, year = random.choice(listToChooseFrom)
    
    #TODO, check whether file still exists

    newImage = editPhotoAndCopyToTemp(image, year)
    #TODO choose several images, make slideshow



#import random
#import time
#import os
#import sys
#
    intervall = 300                # Intervall in Sekunden
#dir = "~/Hintergrundbilder/"   # Bilderverzeichnis
#
#find = os.popen("find " + dir + " -xtype f")
#photos = find.readlines()
#find.close()
#
#random.seed()
#while True:
#    if os.getppid() == 1:                       # nach dem Abmelden beenden
#	sys.exit()
#
## je nach Desktop-Umgebung bitte anpassen!
    system("gsettings set org.gnome.desktop.background picture-uri 'file://" + newImage + "'")  # ab Ubuntu 11.04
#   time.sleep(intervall)

if __name__ == "__main__":
    main()