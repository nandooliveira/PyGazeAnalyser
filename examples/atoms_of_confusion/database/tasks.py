# -*- coding: utf-8 -*-
from easy import get_list
from executions import Execution
from points import Point


class Task:
    @staticmethod
    def by_experiment(experiment_id):
        """query tasks data for a given experiment"""
        return get_list(
            'select * from experiments_task where experiment_id = %s',
            (experiment_id,)
        )

    @staticmethod
    def by_function(function, experiment_id):
        """query tasks data for a given experiment"""
        return get_list(
            "select * from experiments_task where experiment_id = %d and description LIKE '%s%%'",
            (experiment_id, function,)
        )

    @staticmethod
    def all_points(task_id):
        executions = Execution.by_task(task_id)
        points = []

        for execution in executions:
            points += Point.by_execution(execution)

        return points

# list = Task.by_experiment(2)
# print_row_dict_list(list)

# print([d['description'] for d in list])
# print(len(list))
