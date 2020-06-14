#!/usr/bin/python2.7

import os

IMAGES = [
    "AV1.1.jpg",
    "AV1.2.jpg",
    "AV2.1.jpg",
    "AV2.2.jpg",
    "CO1.1.jpg",
    "CO1.2.jpg",
    "CO2.1.jpg",
    "CO2.2.jpg",
    "LACF1.1.jpg",
    "LACF1.2.jpg",
    "LACF2.1.jpg",
    "LACF2.2.jpg",
]

FLIPPED_DIR="./imgs/flipped"

if not os.path.isdir(FLIPPED_DIR):
    os.mkdir(FLIPPED_DIR)

for image in IMAGES:
    command = os.popen("convert -flip ./imgs/%s %s/%s" % (image, FLIPPED_DIR, image))
    print(command.read())
    print(command.close())
