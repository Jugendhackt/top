from numba import jit, float32, int32
from numpy import full
import numpy as np


#@jit(float32(int32[:], int32[:, :], int32[:, :, :], int32[:], int32[:], int32[:], int32[:, :], int32[:, :], int32[:]))
def benchmark(teachers, students, hours, subject, used_room_type, qty_of_room_type, subjects_of_students, subjects_of_teachers, hours_of_teacher):
    """
    Solution Specific: Every index is in the first dimension the id of a course
    :param teachers: the teacher id
    :param students: a list of student ids, filld up with -1
    :param hours: a list of [day, hour] filled with [-1, -1]
    :param subject: the subject id
    :param used_room_type: the room id
    Problem specific: Every first index is the id of the ressource
    :param qty_of_room_type: how many instances of a given roomtype are available?
    :return: the score for the given solution
    """
    # validate input

    assert len(teachers) == len(students) == len(hours) == len(subject) == len(used_room_type)
    num_courses = len(teachers)

    # initialize score
    global_score = 0.0
    num_violations = 0

    # build timetables for each student
    num_students = np.max(students) + 1
    num_teachers = np.max(teachers) + 1
    num_rooms_types = np.max(used_room_type) + 1
    num_subjects = np.max(subject) + 1

    assert num_rooms_types == len(qty_of_room_type)

    timetables_students = full((num_students, 5, 20), -1)
    timetables_teachers = full((num_teachers, 5, 20), -1)
    num_used_room = full((num_rooms_types, 5, 20), 0)

    students_subjects_satisfied = full((num_students, num_subjects), 0)
    for student, subjects in enumerate(subjects_of_students):
        for subject in subjects:
            students_subjects_satisfied[student, subject] = 1

    # iterate over the courses
    for course_id in range(num_courses):

        # make gardening with the checklist
        for student in students[course_id]:
            students_subjects_satisfied[student, course_id] -= 1

        # check wether teacher can teach the subject
        if subject[course_id] in subjects_of_teachers[teachers[course_id]]:
            num_violations += 1

        # honor double time lessons
        for n_hour in range(hours.shape[1] - 1):
            if (hours[course_id, n_hour] - hours[course_id, n_hour + 1] == [0, -1]).all():
                # punish tipple hours
                if n_hour <= hours.shape[1] - 2:
                    if (hours[course_id, n_hour + 1] - hours[course_id, n_hour + 2] == [0, -1]).all():
                        global_score -= 10.0
                global_score += 1.0

        # build timetables for each student
        for student_index in range(num_students):
            student = students[course_id, student_index]
            if student != -1:
                for n_hour in range(hours.shape[1]):
                    day, hour = hours[course_id, n_hour]
                    if day != -1 or hour != -1:
                        if timetables_students[student, day, hour] == -1:
                            timetables_students[student, day, hour] = course_id
                        else:
                            num_violations += 1

        # build timetables for each teacher
        teacher = teachers[course_id]
        for n_hour in range(hours.shape[1]):
            day, hour = hours[course_id, n_hour]
            if day != -1 or hour != -1:
                if timetables_teachers[teacher, day, hour] == -1:
                    timetables_teachers[teacher, day, hour] = course_id
                else:
                    num_violations += 1

        # fill room used data
        room = used_room_type[course_id]
        for n_hour in range(hours.shape[1]):
            day, hour = hours[course_id, n_hour]
            if day != -1 or hour != -1:
                if num_used_room[room, day, hour] >= qty_of_room_type[room]:
                    num_used_room[room, day, hour] += 1
                else:
                    num_violations += 1

    pupil_scores = full((num_students), 0.0)
    # benchmark length of day
    for pupil, timetable in enumerate(timetables_students):
        for day_index, day in enumerate(timetable):
            for hour, course in enumerate(day):
                if course != -1:
                    # punish early and late classes
                    pupil_scores[pupil] -= (hour - 4) ** 2 * (1 if day_index == 5 else .5)
                    # check if

        # punish monday first lesson
        if [0, 0] != -1:
            pupil_scores[pupil] -= 1

    for checklist in students_subjects_satisfied:
        if checklist.any():
            num_violations += 1

    # add the local scores
    global_score += np.std(pupil_scores) * -10.0
    global_score += np.average(pupil_scores) * 2

    return global_score - (num_violations * 100.0)