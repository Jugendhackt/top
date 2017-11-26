from random import randint, choice
import random
from json import dumps


def generate():
    room_counts = [25, 7, 7, 2, 1, 1]
    room_types = []
    for i, cnt in enumerate(room_counts):
        room_types.append({
            "id": i,
            "count": cnt
        })
    rooms = []
    for i, cnt in enumerate(room_counts):
        for j in range(cnt):
            rooms.append({
                "id": i,
                "count": cnt
            })

    subject_types = []
    for i in range(3 * 25):
        subject_types.append({
            "id": i,
            "hoursPerWeek": randint(2, 6),
            "roomType": choice(rooms)
        })

    students = []
    for i in range(randint(100, 1000)):
        students.append({
            "id": i,
            "subjects": [x["id"] for x in random.choices(subject_types, k=10)]
        })

    teachers = []
    for i in range(randint(50, 200)):
        teachers.append({
            "id": i,
            "subjects": [x["id"] for x in random.choices(subject_types, k=2 * 3)],
            "hoursPerWeek": randint(25, 40),
            "blockedHours": [{
                "dayOfWeek": randint(0, 5),
                "hour": randint(0, 10)
            } for _ in range(3)]
        })

    return {
        "teachers": teachers,
        "students": students,
        "subjects": subject_types,
        "roomTypes": room_types
    }
