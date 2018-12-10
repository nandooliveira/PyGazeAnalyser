# analysis script for atoms of confusion experiment
#
# version 2 (10 Dez 2018)

__author__ = "Fernando Oliveira"

# native
import os
import sys

# custom
from pygazeanalyser.gazeplotter import draw_fixations, draw_heatmap, draw_scanpath, draw_raw

# external
import time
import numpy

from database import easy

# # # # #
# CONSTANTS

# DIRECTORIES
# paths
DIR = os.path.dirname(__file__)
IMGDIR = os.path.join(DIR, 'imgs')
PLOTDIR = os.path.join(DIR, 'plots')
OUTPUTFILENAME = os.path.join(DIR, "output.txt")

# check if the image directory exists
if not os.path.isdir(IMGDIR):
    raise Exception("ERROR: no image directory found; path '%s' does not exist!" % IMGDIR)

# check if output directorie exist; if not, create it
if not os.path.isdir(PLOTDIR):
    os.mkdir(PLOTDIR)

# EXPERIMENT SPECS
DISPSIZE = (1920,1080) # (px,px)
SCREENSIZE = (39.9,29.9) # (cm,cm)
SCREENDIST = 61.0 # cm
PXPERCM = numpy.mean([DISPSIZE[0]/SCREENSIZE[0],DISPSIZE[1]/SCREENSIZE[1]]) # px/cm

# # # # # #
# USER DATA

# PARTICIPANTS IDS
user_ids = raw_input(u"Insert users' IDs separated by comma (ex: 1,2,3): ")
PPS = map(int, user_ids.replace(' ', '').split(',')) # exe: PPS = [1, 2]

# BACKGROUND IMAGE
while True:
    background_image = raw_input("\n\nPut the BG file at " + IMGDIR + " folder and type its name here (Make sure it is a jpg file): ") + '.jpg'
    if os.path.exists(os.path.join(IMGDIR, background_image)):
        print "Background image successfully found!..."
        break
    else:
        print "\n\nI did not find the file at, " + str(os.path.join(IMGDIR, background_image))

# # # # #
# READ FILES

# loop through all participants
for participant_id in PPS:
    participant = easy.get_participant(participant_id)
    print("starting data analysis for participant '%s'" % (participant['name']))

    # LOAD POINTS
    print("loading points from database...")
    points = easy.get_points(participant['task1_start'], participant['task1_end'])

    # GAZE DATA
    print("loading gaze data")

    # NEW OUTPUT DIRECTORIES
    # create a new output directory for the current participant
    pplotdir = os.path.join(PLOTDIR, str(participant['name']))

    # check if the directory already exists
    if not os.path.isdir(pplotdir):
        # create it if it doesn't yet exist
        os.mkdir(pplotdir)

    # # # # #
    # PLOTS

    print("plotting gaze data")
    fixations = []
    x_points = []
    y_points = []
    imagefile = os.path.join(IMGDIR, background_image)
    raw_file = os.path.join(pplotdir, 'raw')
    scatter_file = os.path.join(pplotdir, 'fixations')
    scanpath_file = os.path.join(pplotdir, 'scanpath')
    heatmap_file = os.path.join(pplotdir, 'heatmap')

    previous_point = []
    saccades = []

    for point in points:
        x_points.append(point['x'])
        y_points.append(point['y'])
        fixations.append([time.time(), time.time(), 1, int(float(point['x'])), int(float(point['y']))])

        if len(previous_point) != 0:
            saccades.append([time.time(), time.time(), 1, int(float(previous_point['x'])), int(float(previous_point['y'])), int(float(point['x'])), int(float(point['y']))])

        previous_point = point

    draw_raw(x_points, y_points, DISPSIZE, imagefile=imagefile, savefilename=raw_file)
    draw_fixations(fixations, DISPSIZE, imagefile=imagefile, durationsize=True, durationcolour=False, alpha=0.5, savefilename=scatter_file)
    draw_scanpath(fixations, saccades, DISPSIZE, imagefile=imagefile, alpha=0.5, savefilename=scanpath_file)
    draw_heatmap(fixations, DISPSIZE, imagefile=imagefile, durationweight=True, alpha=0.5, savefilename=heatmap_file)
