# analysis script for atoms of confusion experiment
#
# version 2 (10 Dez 2018)

__author__ = "Fernando Oliveira"

# native
import os
# external
import time
from datetime import datetime

# custom
from pygazeanalyser.gazeplotter import draw_fixations, draw_heatmap, draw_raw

# external
import numpy

from database.tasks import Task

os.system('reset')


def c_time():
    return "\033[94m %s \033[0m" % datetime.now().ctime()


# # # # #
# CONSTANTS

# DIRECTORIES
# paths
DIR = os.path.dirname(__file__)
IMGDIR = os.path.join(DIR, 'imgs')
PLOTDIR = os.path.join(DIR, 'plots_puc')

# check if the image directory exists
if not os.path.isdir(IMGDIR):
    raise Exception("ERROR: no image directory found; path '%s' does not exist!" % IMGDIR)

# check if output directories exist; if not, create it
if not os.path.isdir(PLOTDIR):
    os.mkdir(PLOTDIR)

# EXPERIMENT SPECS
DISPSIZE = (1920, 1080)  # (px,px)
SCREENSIZE = (39.9,29.9) # (cm,cm)
SCREENDIST = 61.0 # cm
PXPERCM = numpy.mean([DISPSIZE[0]/SCREENSIZE[0], DISPSIZE[1]/SCREENSIZE[1]])  # px/cm

print('%s: Get task and points' % c_time())

# loop through all tasks
for task in Task.by_experiment(4):
    print("%s: Starting data analysis for task '%s'" % (c_time(), task['description'],))

    print("%s: Loading bg image" % c_time())
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)
    background_image = task['description'] + '.jpg'
    if os.path.exists(os.path.join(IMGDIR, background_image)):
        print("%s: Background image successfully found!" % c_time())
    else:
        raise ValueError("Could not find bg image at %s" % str(os.path.join(IMGDIR, background_image)))

    # LOAD POINTS
    print("%s: Loading points from database" % c_time())
    points = Task.all_points(task['id'])

    # NEW OUTPUT DIRECTORIES
    # create a new output directory for the current participant
    pplotdir = os.path.join(PLOTDIR, str(task['description']))

    # check if the directory already exists
    if not os.path.isdir(pplotdir):
        # create it if it doesn't yet exist
        os.mkdir(pplotdir)

    # # # # #
    # PLOTS

    print("%s: Plotting gaze data" % c_time())
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
        x = int(float(point['x'].replace(',', '.')))
        y = int(float(point['y'].replace(',', '.')))

        x_points.append(x)
        y_points.append(y)

        fixations.append([time.time(), time.time(), 1, x, y])

        # if len(previous_point) != 0:
        #     previous_x = int(float(previous_point['x'].replace(',', '.')))
        #     previous_y = int(float(previous_point['y'].replace(',', '.')))
        #     saccades.append([time.time(), time.time(), 1, previous_x, previous_y, x, y])

        previous_point = point

    print("%s: Generating Heat Map" % c_time())
    draw_heatmap(fixations, DISPSIZE, imagefile=imagefile, durationweight=True, alpha=0.5, savefilename=heatmap_file)

    # print("%s: Generating Raw Chart" % c_time())
    # draw_raw(x_points, y_points, DISPSIZE, imagefile=imagefile, savefilename=raw_file)

    # print("%s: Generating Fixations Map" % c_time())
    # draw_fixations(fixations, DISPSIZE, imagefile=imagefile, durationsize=True, durationcolour=False, alpha=0.5,
    #                savefilename=scatter_file)
    # draw_scanpath(fixations, saccades, DISPSIZE, imagefile=imagefile, alpha=0.5, savefilename=scanpath_file)
