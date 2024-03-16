#!/usr/bin/env python

import json

FIELD_MAP = (
    # field name, column number(s)
    ('ors', '1-2'),
    ('obstacle_number', '4-9'),
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
    ('obstacle_type', '63-80'),
    ('quantity', '82'),
    ('height_agl', '84-88'),
    ('height_amsl', '90-94'),
    ('lighting', '96'),
    ('horiz_accuracy', '98'),
    ('vert_accuracy', '100'),
    ('mark_indicator', '102'),
    ('faa_study_number', '104-117'),
    ('action', '119'),
    ('date_of_action', '121-127')
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
                raise Exception("Parse error: field map column {} must be quoted strings.".format(cols))
            if len(cols) == 2:
                data[key] = line[cols[0]-1:cols[1]].strip()
            elif len(cols) == 1:
                data[key] = line[cols[0]-1].strip()
            else:
                raise Exception("Parse error: field map columns must be either a single int or an int range. ie., '3-4' ")
        return data

    def to_json(self):
        return json.dumps(self.data)


def strip_headers(x):
    x = list(x)
    return x[4:]


if __name__ == '__main__':
    import glob
    import sys

    files = []
    json_out = []
    args = sys.argv
    argc = len(args)
    if argc > 1:
        basename = args.pop(0)
        outfile = args.pop(-1)
        for arg in sys.argv[1:-1]:
            for fn in glob.glob(arg):
                files.append(fn)
        files = list(set(files)) # dedup
    else:
        print("No args specified. Supply one or more infiles, or wildcard. The last argument should be the outfile.")
        exit()
    for fn in files:
        f = open(fn, 'r')
        f = strip_headers(f)
        for ln in f:
            do = DigitalObstacle(ln)
            json_out.append(do.data)
    try:
        fo = open(outfile, 'w')
        fo.write(json.dumps(json_out))
        fo.close()
    except Exception as err:
        raise err
