#!/usr/bin/env python

import glob
import json
import sys

FIELD_MAP = (
    # field name, column number(s)
    ('ors', '1-9'),
    ('verification_status', '11'),
    ('country', '13-14'),
    ('state', '16-17'),
    ('city', '19-34'),
    ('lat_deg', '36-37'),
    ('lat_min', '39-40'),
    ('lat_sec', '42-46'),
    ('lat_hemi', '47'),
    ('long_deg', '49-51'),
    ('long_min', '53-54'),
    ('long_sec', '56-60'),
    ('long_hemi', '61'),
    ('obstacle_type', '63-74'),
    ('quantity', '76'),
    ('height_agl', '78-82'),
    ('height_amsl', '84-88'),
    ('lighting', '90'),
    ('horiz_accuracy', '92'),
    ('vert_accuracy', '94'),
    ('mark_indicator', '96'),
    ('faa_study_number', '98-111'),
    ('action', '113'),
    ('date_of_action', '115-121')
)

class DigitalObstacle(object):
    def __init__(self, line, field_map=FIELD_MAP):
        self.field_map = field_map
        self.data = self._parse(line)

    def _parse(self, line):
        data = {}
        for key, columns in self.field_map:
            try:
                cols = [int(col) for col in columns.split('-')]
            except AttributeError:
                raise Exception("Parse error: field map columns must me quotes strings.")
            if len(cols) == 2:
                data[key] = line[cols[0]-1:cols[1]].strip()
            elif len(cols) == 1:
                data[key] = line[cols[0]].strip()
            else:
                raise Exception("Parse error: field map columns must be either a single int or an int range. ie., '3-4' ")
        return data

    def to_json(self):
        return json.dumps(self.data)


def strip_headers(x):
    return x[4:]


if __name__ == '__main__':
    files = []
    json_out = []
    try:
        for arg in sys.argv[1:-1]:
            for fn in glob.glob(arg):
                files.append(fn)
        files = list(set(files))
    except:
        raise Exception("You must specify a DOF file, list of files, or wildcards to process.")
    for fn in files:
        f = open(fn, 'r')
        f = strip_headers(list(f))
        for ln in f:
            do = DigitalObstacle(ln)
            json_out.append(do.data)
    try:
        fo = open(sys.argv[-1],'w')
        fo.write(json.dumps(json_out))
        fo.close()
    except Exception as err:
        raise err



