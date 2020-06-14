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
from pygazeanalyser.detectors import fixation_detection
from pygazeanalyser.gazeplotter import draw_fixations

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
    for point in points:
        x_points.append(int(float(point['x'].replace(',', '.'))))
        y_points.append(int(float(point['y'].replace(',', '.'))))
        time_points.append(calendar.timegm(point['datetime'].timetuple()))

    fixations_data = fixation_detection(np.array(x_points), np.array(y_points), np.array(time_points), maxdist=20, mindur=200)

    fixations = map(lambda fixation: {'x': fixation[3], 'y': fixation[4], 'timestamp': fixation[1]}, fixations_data[1])

    json_dict[execution['task_description']][execution['participant_name']]['fixations'] = fixations

    # chart
    background_image = execution['task_description'] + '.jpg'
    imagefile = os.path.join(IMGDIR, background_image)
    scatter_file = os.path.join(DATADIR, "fixations %s %s.png" % (execution['participant_name'], execution['task_description']))
    draw_fixations(fixations_data[1], DISPSIZE, imagefile=imagefile, durationsize=True, durationcolour=False, alpha=0.5,
                   savefilename=scatter_file)

json_file_path = os.path.join(DATADIR, 'fixations.json')
f = open(json_file_path, "a")
f.write(json.dumps(json_dict))
f.close()
print json.dumps(json_dict)

