# -*- coding: utf-8 -*-

#!/usr/bin/env python
import argparse
from datetime import datetime
from time import sleep
from itertools import izip
from os import system, path, getppid
from PIL import Image, ImageDraw, ImageFont
from sys import exit
import random

intervall = 600                # Period of slide show in seconds
    
parser = argparse.ArgumentParser(description='Search in the DB to give back an image from the same day some years ago')
parser.add_argument('file', type=str,
                   help="the file where the fotobase will be read from")
parser.add_argument('--shuffle',  action="store_true", default=False,
                   help="single reshuffle of wallpaper (if you dont like it)")


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
            if path.isfile(f):
                print "{} was shot the same day {} years ago".format(f,today.year-t.year)
                listToChooseFrom.append( (f, t.year))
    
    if len(listToChooseFrom)==0:
        exit();        
    
    
    while True:
        if getppid() == 1:                       # nach dem Abmelden beenden
            exit()
        
        image, year = random.choice(listToChooseFrom)
        if path.isfile(image):
            newImage = editPhotoAndCopyToTemp(image, year)
            system("gsettings set org.gnome.desktop.background picture-uri 'file://" + newImage + "'")  # ab Ubuntu 11.04
        if args.shuffle:
            exit()
            break
        sleep(intervall)

if __name__ == "__main__":
    main()
