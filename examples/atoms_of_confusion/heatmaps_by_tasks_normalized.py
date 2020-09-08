# analysis script for atoms of confusion experiment
#
# version 2 (10 Dez 2018)

__author__ = "Fernando Oliveira"

# native
import os
import calendar
from datetime import datetime, timedelta

# external
import numpy as np

from database.tasks import Task
# custom
from pygazeanalyser.gazeplotter import draw_heatmap

os.system('reset')


def c_time():
    return "\033[94m %s \033[0m" % datetime.now().ctime()


# # # # #
# CONSTANTS

# DIRECTORIES
# paths
DIR = os.path.dirname(__file__)
DATADIR = os.path.join(DIR, 'data')
IMGDIR = os.path.join(DIR, 'imgs/flipped')
PLOTDIR = os.path.join(DIR, 'plots_puc')

# check if the image directory exists
if not os.path.isdir(IMGDIR):
    raise Exception("ERROR: no image directory found; path '%s' does not exist!" % IMGDIR)

# check if output directories exist; if not, create it
if not os.path.isdir(PLOTDIR):
    os.mkdir(PLOTDIR)

# EXPERIMENT SPECS
DISPSIZE = (1920, 1080)  # (px,px)
SCREENSIZE = (39.9, 29.9)  # (cm,cm)
SCREENDIST = 61.0  # cm
PXPERCM = np.mean([DISPSIZE[0] / SCREENSIZE[0], DISPSIZE[1] / SCREENSIZE[1]])  # px/cm


def heatmap_for_task(task, points):
    print("%s: Starting data analysis for task '%s'" % (c_time(), task['description'],))

    print("%s: Loading bg image" % c_time())
    background_image = task['description'] + '.jpg'
    if os.path.exists(os.path.join(IMGDIR, background_image)):
        print("%s: Background image successfully found!" % c_time())
    else:
        raise ValueError("Could not find bg image at %s" % str(os.path.join(IMGDIR, background_image)))

    # NEW OUTPUT DIRECTORIESm,
    # create a new output directory for the current participant
    pplotdir = os.path.join(PLOTDIR, 'normalized_heatmaps_by_task')

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
    heatmap_file = os.path.join(pplotdir, "heatmap %s.png" % str(task['description']))

    for point in points:
        x = int(float(point['x'].replace(',', '.')))
        y = int(float(point['y'].replace(',', '.')))

        x_points.append(x)
        y_points.append(y)

        timestamp = calendar.timegm(point['datetime'].timetuple())
        fixations.append([timestamp, timestamp + 100, 1, x, y])

    print("%s: Generating Heat Map" % c_time())
    draw_heatmap(fixations, DISPSIZE, imagefile=imagefile, durationweight=False, alpha=0.5, savefilename=heatmap_file)

print('%s: Get task and points' % c_time())

functions = ['AV1', 'AV2', 'CO1', 'CO2', 'LACF1', 'LACF2']
for function in functions:
    tasks = Task.by_function(function, 4)

    tasks_points = {}
    for task in tasks:
        print(task['description'])
        tasks_points[task['description']] = {'points': None, 'count': 0}
        tasks_points[task['description']]['points'] = Task.all_points(task['id'])
        tasks_points[task['description']]['count'] = len(tasks_points[task['description']]['points'])

    higher_task = None
    smaller_task = None
    if tasks_points[tasks[0]['description']]['count'] > tasks_points[tasks[1]['description']]['count']:
        higher_task = tasks_points[tasks[0]['description']]
        smaller_task = tasks_points[tasks[1]['description']]
    elif tasks_points[tasks[0]['description']]['count'] < tasks_points[tasks[1]['description']]['count']:
        higher_task = tasks_points[tasks[1]['description']]
        smaller_task = tasks_points[tasks[0]['description']]
    else:
        higher_task = None
        smaller_task = None

    # normalize
    if higher_task is not None or smaller_task is not None:
        for i in range(0, (higher_task['count'] - smaller_task['count'])):
            last = smaller_task['points'][-1]
            datetimee = last['datetime'] + timedelta(0, 1)
            smaller_task['points'].append({'x': '1000000', 'y': '10000000', 'datetime': datetimee})

    for task in tasks:
        heatmap_for_task(task, tasks_points[task['description']]['points'])
