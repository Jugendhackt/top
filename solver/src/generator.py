import sys
import numpy
import json
from numpy import int32


def parse_teachers(json_data):
    teacher_list = []
    for teacher in json_data["teachers"]:
        teacher_list.append([teacher["id"], [subject for subject in teacher["subjects"]], teacher["hoursPerWeek"],
                             [[time["dayOfWeek"] for time in teacher["blockedHours"]],
                              [time["hour"] for time in teacher["blockedHours"]]]])
    return teacher_list


def parse_students(json_data):
    student_list = []
    for student in json_data["students"]:
        student_list.append([student["id"], [subject for subject in student["subjects"]]])
    return student_list


def parse_subjects(json_data):
    subject_list = []
    for subject in json_data["subjects"]:
        subject_list.append([subject["id"], subject["hoursPerWeek"]])


def parse_rooms(json_data):
    room_list = []
    for room in json_data["roomTypes"]:
        room_list.append([room["id"], room["count"]])
    return room_list


def extract_data(json_data):
    teachers = parse_teachers(json_data)
    students = parse_students(json_data)
    subjects = parse_subjects(json_data)
    rooms = parse_rooms(json_data)


"""
[[lehrern], [schülern], [räumen], [kursen]]

lehrer = [[fächern], [[tag, zeit]], wochenstunden, id]
schüler = [[fächer], id]
raum = [typ, anzahl]
kurs = [raumbedarf, id]

 """


def generate(constraints):
    pass


def mutate(probability=.1):
    pass
