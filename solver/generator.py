import sys
import numpy
import json
from numpy import int32

def parse_teachers(json_data):
    teacher_list = []
    for teacher in json_data["teachers"]:
        teacher_id = teacher["id"]
        subjects = [subject for subject in teacher["subjects"]]
        hours_per_week = teacher["hoursPerWeek"]
        blocked_hours = [[time["dayOfWeek"] for time in teacher["blockedHours"]], [time["hour"] for time in teacher["blockedHours"]]]
        teacher_list.append([teacher_id, subjects, hours_per_week, blocked_hours])
    return teacher_list

#def parse_students(json_data):


def extract_data(json_data):
    teachers = parse_teachers(json_data)

parse_teachers(json.load(sys.stdin))
"""
[[lehrern], [schülern], [räumen], [kursen]]

lehrer = [[fächern], [[tag, zeit]], wochenstunden, id]
schüler = [[fächer], id]
raum = [typ, anzahl]
kurs = [raumbedarf, id]

 """

#NOTE from here on there will be only CUDA compatible code

#def generate_random_timetable(json_data, seed = 0):
