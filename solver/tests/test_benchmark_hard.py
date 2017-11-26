import numpy as np

from src.benchmark import benchmark

correct_teachers = np.array([0])
correct_students = np.array([[0]])
correct_hour = np.full((1,1,2), -1)
correct_subjects = np.array([0])
correct_used_room_type = np.array([0])
correct_qty_of_room = np.array([1])
correct_subjects_of_students = np.full((1,1), 0)
correct_subjects_of_teachers = np.full((1,1), 0)
correct_hours_of_teacher = np.array([10])

wrong_qty_of_rooms = np.array([0])

#sig: def benchmark(teachers, students, hours, subject, used_room_type, qty_of_room_type)
def test_all_hards_valid():
    assert len(correct_teachers) == len(correct_students) == len(correct_hour) == len(correct_subjects) == len(correct_used_room_type)
    test_var = benchmark(correct_teachers, correct_students, correct_hour, correct_subjects, correct_used_room_type, correct_qty_of_room, correct_subjects_of_students, correct_subjects_of_teachers, correct_hours_of_teacher)
    assert test_var < 100

def test_qty_of_rooms_invalid():
    assert len(correct_teachers) == len(correct_students) == len(correct_hour) == len(correct_subjects) == len(correct_used_room_type)
    test_var = benchmark(correct_teachers, correct_students, correct_hour, correct_subjects, correct_used_room_type, wrong_qty_of_rooms, correct_subjects_of_students, correct_subjects_of_teachers, correct_hours_of_teacher)
    assert abs(test_var) > 100
