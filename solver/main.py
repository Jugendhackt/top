#!/usr/bin/env python3

import sys
import json

import jsonschema


def validate_contents(json_data):
    subject_ids = {s["id"] for s in json_data["subjects"]}
    student_subject_ids = {subject for student in json_data["students"] for subject in student["subjects"]}
    teacher_subject_ids = {subject for teacher in json_data["teachers"] for subject in teacher["subjects"]}
    if len((student_subject_ids | teacher_subject_ids) - subject_ids) != 0:
        raise ValueError("not all needed subjects exist!")

    room_ids = {r["id"] for r in json_data["roomTypes"]}
    subject_room_ids = {r["roomType"] for r in json_data["subjects"]}
    if len(subject_room_ids - room_ids) != 0:
        raise ValueError("not all needed rooms exist!")

    room_count = {r["count"] for r in json_data["roomTypes"]}
    if 0 in room_count:
        raise ValueError("there is a room which exists zero times!")


if __name__ == "__main__":
    # read input data
    input_data = json.load(sys.stdin)

    # validate the input
    with open('input_schema.json') as f:
        input_schema = json.load(f)
    jsonschema.validate(input_data, input_schema)
    validate_contents(input_data)

    # TODO: solve

    # output the solution
    print(input_data)
