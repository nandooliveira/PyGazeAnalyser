# -*- coding: utf-8 -*-
import pprint
import psycopg2
import psycopg2.extras

pp = pprint.PrettyPrinter(indent=4)

def print_row_dict_list(list):
    for row_dict in list:
        print('---------------------------')
        for key in row_dict.keys():
            print("%s: %s" % (key, row_dict.get(key)))

    print('---------------------------')


def get_connection():
    return psycopg2.connect("dbname=easy host=127.0.0.1 user=postgres password=postgres")


def run_with_cursor(query_func):
    """Get a database cursor"""
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return query_func(cur)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

        if cur is not None:
            cur.close()


def get_single_result(query, params):
    def query_func(cur):
        cur.execute(query % params)
        row = cur.fetchone()

        return row

    return run_with_cursor(query_func)


def get_list(query, params=tuple()):
    def query_func(cur):
        cur.execute(query % params)
        row = cur.fetchone()
        rows = []

        while row is not None:
            rows.append(row)
            row = cur.fetchone()

        return rows

    return run_with_cursor(query_func)


def get_participant(participant_id):
    """ query data from the vendors table """

    return get_single_result(
        "SELECT id, name, email, flow, start_datetime, end_datetime, task1_start, task1_end, task2_start, task2_end FROM experiments_participant WHERE id = %s ORDER BY id desc",
        (participant_id,)
    )


def get_points(start_datetime, end_datetime):
    """ query data from the vendors table """
    return get_list(
        "SELECT * FROM experiments_point WHERE datetime between '%s' and '%s' ORDER BY id desc",
        (start_datetime, end_datetime,)
    )
