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
from database.tasks import Task
from database.points import Point

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

# BACKGROUND IMAGE
while True:
    background_image = raw_input("\n\nPut the BG file at " + IMGDIR + " folder and type its name here (Make sure it is a jpg file): ") + '.png'
    if os.path.exists(os.path.join(IMGDIR, background_image)):
        print "Background image successfully found!..."
        break
    else:
        print "\n\nI did not find the file at, " + str(os.path.join(IMGDIR, background_image))


print 'get task and points..\n'

# loop through all tasks
for task in Task.by_experiment(2):
    print("starting data analysis for task '%s'" % (task['description']))

    # LOAD POINTS
    print("loading points from database...")
    points = Task.all_points(task['id'])

    # GAZE DATA
    print("loading gaze data")

    # NEW OUTPUT DIRECTORIES
    # create a new output directory for the current participant
    pplotdir = os.path.join(PLOTDIR, str(task['description']))

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
        x = float(point['x'].replace(',', '.'))
        y = float(point['y'].replace(',', '.'))
        print "%f %f" % (x, y,)

        x_points.append(x)
        y_points.append(y)

        fixations.append([time.time(), time.time(), 1, x, y])

        if len(previous_point) != 0:
            previous_x = float(previous_point['x'].replace(',', '.'))
            previous_y = float(previous_point['y'].replace(',', '.'))
            saccades.append([time.time(), time.time(), 1, previous_x, previous_y, x, y])

        previous_point = point

    draw_heatmap(fixations, DISPSIZE, imagefile=imagefile, durationweight=True, alpha=0.5, savefilename=heatmap_file)
    draw_raw(x_points, y_points, DISPSIZE, imagefile=imagefile, savefilename=raw_file)
    draw_fixations(fixations, DISPSIZE, imagefile=imagefile, durationsize=True, durationcolour=False, alpha=0.5, savefilename=scatter_file)
    draw_scanpath(fixations, saccades, DISPSIZE, imagefile=imagefile, alpha=0.5, savefilename=scanpath_file)
