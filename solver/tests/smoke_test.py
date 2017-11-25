from subprocess import Popen, PIPE
from shlex import split


def test_fail_on_invalid_schema():
    with open("tests/json/schema_fault.json") as f:
        invalid_schema = f.read()

    print(invalid_schema)

    p = Popen(split("./solver"), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(invalid_schema.encode("UTF-8"))

    assert stdout.decode("UTF-8") == ""
    assert "Traceback" in stderr.decode("UTF-8")


def test_fail_on_invalid_semantic():
    with open("tests/json/semantic_fault.json") as f:
        invalid_schema = f.read()

    print(invalid_schema)

    p = Popen(split("./solver"), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(invalid_schema.encode("UTF-8"))

    assert stdout.decode("UTF-8") == ""
    assert "Traceback" in stderr.decode("UTF-8")


def test_valid_output():
    raise NotImplementedError
