import sys
import json

import jsonschema

def validate_contents(json_data):
    subject_ids = {s["id"] for s in json_data["subjects"]}
    student_subject_ids = {subject for student in json_data["students"] for subject in student["subjects"]}
    teacher_subject_ids = {subject for teacher in json_data["teachers"] for subject in teacher["subjects"]}
    if len((student_subject_ids | teacher_subject_ids) - subject_ids) == 0:
        print("yay")
    else:
        print("nay")

if __name__ == "__main__":
    with open('input_schema.json') as f:
        input_schema = json.load(f)

    input_data = json.load(sys.stdin)

    jsonschema.validate(input_data, input_schema)

    validate_contents(input_data)
