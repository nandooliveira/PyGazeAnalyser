# -*- coding: utf-8 -*-
from easy import get_list, print_row_dict_list


class Task():
    @staticmethod
    def by_experiment(experiment_id):
        """query tasks data for a given experiment"""
        return get_list(
            'select * from experiments_task where experiment_id = %s',
            (experiment_id,)
        )


# list = Task.by_experiment(2)
# print_row_dict_list(list)

# print([d['description'] for d in list])
# print(len(list))
