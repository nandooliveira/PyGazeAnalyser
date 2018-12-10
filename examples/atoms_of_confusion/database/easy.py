# -*- coding: utf-8 -*-
import psycopg2
import psycopg2.extras

def get_connection():
    return psycopg2.connect("dbname=easy user=postgres password=postgres")

def get_participant(participant_id):
    """ query data from the vendors table """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT id, name, email, flow, start_datetime, end_datetime, task1_start, task1_end, task2_start, task2_end FROM experiments_participant WHERE id = %s ORDER BY id desc" % participant_id)
        row = cur.fetchone()

        cur.close()

        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def get_points(start_datetime, end_datetime):
    """ query data from the vendors table """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM experiments_point WHERE datetime between '%s' and '%s' ORDER BY id desc" % (start_datetime, end_datetime))
        row = cur.fetchone()
        rows = []

        while row is not None:
            rows.append(row)
            row = cur.fetchone()

        cur.close()

        return rows
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

