# -*- coding: utf-8 -*-
from easy import get_single_result, print_row_dict_list


class Execution():
    @staticmethod
    def by_participant(participant_id):
        """query executions data for a given participant"""
        return get_list(
            'select id, start, "end", participant_id, task_id, number_of_errors from experiments_execution where participant_id = %s',
            (participant_id,)
        )

    @staticmethod
    def by_task(task_id):
        """query executions data for a given task"""
        return get_list(
            'select * from experiments_execution where task_id = %s',
            (task_id,)
        )

    @staticmethod
    def by_id(id):
        """query executions data for a given task"""
        return get_single_result(
            'select * from experiments_execution where id = %s',
            (id,)
        )


# list = Execution.by_task(14)
# print_row_dict_list(list)

# print(len(list))
