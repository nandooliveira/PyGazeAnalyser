# analysis script for atoms of confusion experiment
#
# version 2 (10 Dez 2018)

__author__ = "Fernando Oliveira"

# native
import os
from datetime import datetime
import calendar
import json

# custom
import numpy as np

from database.executions import Execution
from database.points import Point

# external
from pygazeanalyser.detectors import fixation_detection, saccade_detection
from pygazeanalyser.gazeplotter import draw_fixations, draw_scanpath

os.system('reset')


def c_time():
    return "\033[94m %s \033[0m" % datetime.now().ctime()


# # # # #
# CONSTANTS

# DIRECTORIES
# paths
DIR = os.path.dirname(__file__)
DATADIR = os.path.join(DIR, 'data')
DISPSIZE = (1920, 1080)
BASE_IMG_DIR = os.path.join(DIR, 'imgs')
IMGDIR = os.path.join(DIR, 'imgs/flipped')

print('%s: Get executions and points' % c_time())
# loop through all executions
executions = Execution.by_experiment(4)
json_dict = {}
for execution in executions:
    if execution['task_description'] not in json_dict.keys():
        json_dict[execution['task_description']] = {}

    if execution['participant_name'] not in json_dict[execution['task_description']].keys():
        json_dict[execution['task_description']][execution['participant_name']] = {}

    points = Point.by_execution(execution)
    print(len(points))
    # Fixations
    x_points, y_points, time_points = [], [], []

    fixations = []

    for point in points:
        x_points.append(int(float(point['x'].replace(',', '.'))))
        y_points.append(int(float(point['y'].replace(',', '.'))))
        time_points.append(calendar.timegm(point['datetime'].timetuple()))

    fixations_data = fixation_detection(np.array(x_points), np.array(y_points), np.array(time_points), maxdist=500, mindur=50)
    saccades_data = saccade_detection(np.array(x_points), np.array(y_points), np.array(time_points), missing=0.0, minlen=5, maxvel=100, maxacc=500)

    json_dict[execution['task_description']][execution['participant_name']]['fixations'] = fixations_data[1]
    json_dict[execution['task_description']][execution['participant_name']]['saccades'] = saccades_data[1]

for task_description in json_dict:
    task_dict = json_dict[task_description]

    for participant_name in task_dict:
        participant_fixations = task_dict[participant_name]['fixations']
        participant_saccades  = task_dict[participant_name]['saccades']

        # chart
        background_image = execution['task_description'] + '.jpg'
        imagefile = os.path.join(IMGDIR, background_image)
        # scatter_file = os.path.join(BASE_IMG_DIR, 'newtest', "fixations %s %s.png" % (execution['participant_name'], execution['task_description']))
        scatter_file = os.path.join(BASE_IMG_DIR, 'newtest', "fixations %s %s.png" % (participant_name, task_description))
        draw_fixations(participant_fixations, DISPSIZE, imagefile=imagefile, durationsize=False, durationcolour=False, alpha=0.5,
                       savefilename=scatter_file)
        # scanpath
        scanpathfile = os.path.join(BASE_IMG_DIR, 'newtest', "scanpath %s %s.png" % (participant_name, task_description))
        draw_scanpath(participant_fixations, participant_saccades, DISPSIZE, imagefile=imagefile, alpha=0.5, savefilename=scanpathfile)

# json_file_path = os.path.join(DATADIR, 'fixations.json')
# f = open(json_file_path, 'a')
# f.write(json.dumps(json_dict))
# f.close()
# print json.dumps(json_dict)

