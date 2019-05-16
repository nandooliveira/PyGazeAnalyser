# -*- coding: utf-8 -*-
from easy import get_list


class Pause():
    @staticmethod
    def by_execution(execution_id):
        """query pauses data for a given execution"""
        return get_list(
            "select * from experiments_pause where execution_id = %d",
            (execution_id,)
        )


# list = Pause.by_execution(268)
# print_row_dict_list(list)

# # print([d['description'] for d in list])
# # print(len(list))
