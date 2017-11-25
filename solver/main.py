import sys
import json

import jsonschema


if __name__ == "__main__":
    with open('input_schema.json') as f:
        input_schema = json.load(f)

    input_data = json.load(sys.stdin)

    jsonschema.validate(input_data, input_schema)
