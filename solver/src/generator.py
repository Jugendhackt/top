import sys
import numpy
import random
import json
from numpy import int32

import generate_data

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
    # construct the static env
    hours_of_teachers = []
    subjects_of_teachers = []
    for teacher in constraints["teachers"]:
        hours_of_teachers.append(teacher["hoursPerWeek"])
        subjects_of_teachers.append(teacher["subjects"])# has a list of subjects for the teacher id = index

    subjects_of_students = []
    for student in constraints["students"]:
        subjects_of_students.append(student["subjects"])

    qty_of_room_type = []
    for room_type in constraints["roomTypes"]:
        qty_of_room_type.append(room_type["count"])

    # construct a random solution
    solution = []
    all_the_subjects = []
    for s in subjects_of_students:
        all_the_subjects += s
    subject_ranking = numpy.bincount(all_the_subjects)
    subject_ranking = sorted(enumerate(subject_ranking), key=lambda x:x[1])
    subjects_and_who_teaches_them = [] #list of teachers that can teach the subject with id = index
    for subject in set(all_the_subjects):
        subjects_and_who_teaches_them.append((subject, []))
    for tid in range(len(subjects_of_teachers)):
        for subject in subjects_of_teachers[tid]:
            subjects_and_who_teaches_them[subjects_and_who_teaches_them.index(subject)]
    for subject in subject_ranking:
        pass
    result = []
    return result


def mutate(input_data, inverse_intensity=1):
    #input = [teacher, students, hours, subject, used_room_type, qty_of_room_type, subjects_of_students, subjects_of_teachers, hours_of_teachers]
    for course in range(len(input_data[0])):
        if random.randint(0, 3 * inverse_intensity) >= 3 * inverse_intensity: #randomly decide to swap a teacher or not
            partner = random.randint(0, len(input_data[0]))
            input_data[0][course], input_data[0][partner] = input_data[0][partner], input_data[0][course]
        if random.randint(0, 5 * inverse_intensity) >= 5 * inverse_intensity:#give one teacher more todo
            input_data[0][course] = input_data[0][random.randint(0, len(input_data[0]))]

    result = input

    return result

generate(generate_data.generate())