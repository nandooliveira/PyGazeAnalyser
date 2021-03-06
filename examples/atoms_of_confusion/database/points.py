# -*- coding: utf-8 -*-
import pytz
from easy import get_list, print_row_dict_list
from executions import Execution
from pauses import Pause


class Point():
    @staticmethod
    def by_execution(execution):
        """query points data for a given execution"""
        if execution['start'] is None or execution['end'] is None:
            return []

        utc = pytz.UTC
        pattern = "%Y-%m-%d %H:%M:%S"
        # start = execution['start'].astimezone(utc).strftime(pattern)
        # end = execution['end'].astimezone(utc).strftime(pattern)
        start = execution['start'].strftime(pattern) # .astimezone(utc).strftime(pattern)
        end = execution['end'].strftime(pattern) #.astimezone(utc).strftime(pattern)

        list = get_list(
            "select * from experiments_point where datetime between '%s' and '%s' order by id asc",
            (start, end,)
        )

        return Point.__remove_points_in_pauses_interval(list, execution)

    @staticmethod
    def __is_point_inside_pause(point, pause):
        if pause['start_time'] is None or pause['end_time'] is None:
            return False

        utc = pytz.UTC
        pattern = "%Y-%m-%d %H:%M:%S"
        pause_start = pause['start_time'].strftime(pattern) #.astimezone(utc).strftime(pattern)
        pause_end = pause['end_time'].strftime(pattern) # .astimezone(utc).strftime(pattern)
        datetime = point['datetime'].strftime(pattern)

        return datetime >= pause_start and datetime <= pause_end

    @staticmethod
    def __remove_points_in_pauses_interval(points, execution):
        pauses = Pause.by_execution(execution['id'])
        results = []
        for point in points:
            should_add = True
            for pause in pauses:
                if Point.__is_point_inside_pause(point, pause):
                    should_add = False

            if should_add:
                results.append(point)

        return results


# execution = Execution.by_id(13)
# list = Point.by_interval(execution)
# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(len(list))

# quantidade total:
# quantidade filtrando: 22013
# print_row_dict_list(list)

# print([d['description'] for d in list])
# print(len(list))
