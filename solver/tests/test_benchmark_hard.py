import numpy as np
from numpy import int32

from benchmark import benchmark

correct_teachers = np.array([0])
correct_students = np.array([[0]])
correct_hour = np.full(3, -1)
correct_subjects = np.array([0])
correct_used_room_type = np.array([0])
correct_qty_of_room = np.array([1])


#sig: def benchmark(teachers, students, hours, subject, used_room_type, qty_of_room_type)
def test_all_hards_valid():
    test_var = benchmark(correct_teachers, correct_students, correct_hour, correct_subjects, correct_used_room_type, correct_qty_of_room)
    assert test_var < 100, "fuck"