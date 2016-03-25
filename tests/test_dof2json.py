import json
from dof2json import dof2json

DOF_FILE = './tests/fixtures/test_dof.Dat'
JSON_FILE = './tests/fixtures/test_dof.json'

def test_strip_headers():
    f = open(DOF_FILE, 'r')
    for i, l in enumerate(f, 1):
        pass
    assert i == 7
    f.seek(0)
    o = dof2json.strip_headers(f)
    assert len(o) == 3

def test_dof2json():
    json_out = []
    j = open(JSON_FILE, 'r')
    json_list = json.loads(j.read())
    f = open(DOF_FILE, 'r')
    f = dof2json.strip_headers(f)
    for line in f:
        do = dof2json.DigitalObstacle(line)
        json_out.append(json.loads(do.to_json()))
    assert cmp(json_list, json_out) == 0
