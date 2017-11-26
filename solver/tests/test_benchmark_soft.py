import numpy as np
from numpy import int32

from benchmark import benchmark


def test_honor_double():
    teacher1 = np.full((1), 0, dtype=int32)
    pupils1 = np.full((1, 1), 0, dtype=int32)
    hours1 = np.array([[
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
        [-1, -1],
        [-1, -1]
    ]])
    subject1 = np.full((1), 0, dtype=int32)
    room_type1 = np.full((1), 0, dtype=int32)

    teacher2 = np.full((1), 0, dtype=int32)
    pupils2 = np.full((1, 1), 0, dtype=int32)
    hours2 = np.array([[
        [0, 0],
        [1, 0],
        [1, 3],
        [2, 0],
        [-1, -1],
        [-1, -1]
    ]])
    subject2 = np.full((1), 0, dtype=int32)
    room_type2 = np.full((1), 0, dtype=int32)

    assert benchmark(teacher1, pupils1, hours1, subject1, room_type1, [1]) >\
           benchmark(teacher2, pupils2, hours2, subject2, room_type2, [1])


def test_punish_tripple():
    teacher1 = np.full((1), 0, dtype=int32)
    pupils1 = np.full((1, 1), 0, dtype=int32)
    hours1 = np.array([[
        [0, 0],
        [0, 1],
        [0, 2],
        [1, 0],
        [1, 1],
        [-1, -1],
        [-1, -1]
    ]])
    subject1 = np.full((1), 0, dtype=int32)
    room_type1 = np.full((1), 0, dtype=int32)

    teacher2 = np.full((1), 0, dtype=int32)
    pupils2 = np.full((1, 1), 0, dtype=int32)
    hours2 = np.array([[
        [0, 0],
        [0, 3],
        [0, 1],
        [1, 0],
        [1, 3],
        [-1, -1],
        [-1, -1]
    ]])
    subject2 = np.full((1), 0, dtype=int32)
    room_type2 = np.full((1), 0, dtype=int32)

    assert benchmark(teacher1, pupils1, hours1, subject1, room_type1, [1]) <\
           benchmark(teacher2, pupils2, hours2, subject2, room_type2, [1])


def test_punish_long_days():
    teacher1 = np.full((1), 0, dtype=int32)
    pupils1 = np.full((1, 1), 0, dtype=int32)
    hours1 = np.array([[
        [0, 0],
        [0, 1],
        [0, 7],
        [1, 0],
        [1, 8],
        [-1, -1],
        [-1, -1]
    ]])
    subject1 = np.full((1), 0, dtype=int32)
    room_type1 = np.full((1), 0, dtype=int32)

    teacher2 = np.full((1), 0, dtype=int32)
    pupils2 = np.full((1, 1), 0, dtype=int32)
    hours2 = np.array([[
        [0, 0],
        [0, 3],
        [0, 1],
        [1, 0],
        [1, 3],
        [-1, -1],
        [-1, -1]
    ]])
    subject2 = np.full((1), 0, dtype=int32)
    room_type2 = np.full((1), 0, dtype=int32)

    assert benchmark(teacher1, pupils1, hours1, subject1, room_type1, [1]) <\
           benchmark(teacher2, pupils2, hours2, subject2, room_type2, [1])

