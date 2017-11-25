from numba import jit, float32, int32
from numpy import full
import numpy as np


# @jit(float32(int32[:], int32[:, :], int32[:, :, :], int32[:], int32[:]))
def benchmark(teacher, pupils, hours, subject, room_type):
    # validate input
    """

    Every list is in the first dimension the list of couses
    :param teacher: the teacher id
    :param pupils: a list of student ids, filld up with -1
    :param hours: a list of [day, hour] filled with [-1, -1]
    :param subject: the subject id
    :param room_type: the room id
    :return: the score for the given solution
    """

    assert len(teacher) == len(pupils) == len(hours) == len(subject) == len(room_type)
    num_couses = len(teacher)

    # initialize score
    global_score = 0.0

    # build timetables for each student
    num_pupils = np.max(pupils) + 1
    timetables = full((num_pupils, 5, 20), -1)

    # iterate over the courses
    for course_id in range(num_couses):

        # honor double time lessons
        for n_hour in range(hours.shape[1] - 1):
            if (hours[course_id, n_hour] - hours[course_id, n_hour + 1] == [0, -1]).all():
                # punish tipple hours
                if n_hour <= hours.shape[1] - 2:
                    if (hours[course_id, n_hour + 1] - hours[course_id, n_hour + 2] == [0, -1]).all():
                        global_score -= 10.0
                global_score += 1.0

        # build timetables for each student
        for student_index in range(num_pupils):
            student = pupils[course_id, student_index]
            if student != -1:
                for n_hour in range(hours.shape[1]):
                    day, hour = hours[course_id, n_hour]
                    if day != -1 or hour != -1:
                        timetables[student, day, hour] = course_id

    pupil_scores = full((num_pupils,), 0.0)
    # benchmark length of day
    for pupil, timetable in enumerate(timetables):
        for day_index, day in enumerate(timetable):
            for hour, course in enumerate(day):
                if course != -1:
                    pupil_scores[pupil] -= (hour - 4) ** 2 * (1 if day_index == 5 else .5)

        # punish monday first lesson
        if [0, 0] != -1:
            pupil_scores[pupil] -= 1

    # add the local scores
    global_score += np.std(pupil_scores) * -10.0
    global_score += np.average(pupil_scores) * 2

    return global_score
