# -*- coding: utf-8 -*-
from easy import get_single_result, print_row_dict_list, get_list


class Execution():
    @staticmethod
    def by_experiment(experiment_id):
        """All execution of a experiment"""
        return get_list("""
            SELECT
                experiments_execution.id,
                et.description AS task_description,
                UPPER(ep.name) AS participant_name,
                start,
                "end"
            FROM experiments_execution
                INNER JOIN experiments_task et ON experiments_execution.task_id = et.id
                INNER JOIN experiments_participant ep ON experiments_execution.participant_id = ep.id
                WHERE et.experiment_id = %d
        """, experiment_id)

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
            'select * from experiments_execution where task_id = %s and participant_id not in(185, 171, 169)',
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
