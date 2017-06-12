from contentful import Client
import json
import jsonpickle
import os
import pdb

# config where files are stored
OUT_DIR = 'data'
EVENT = 'event'
TAG = 'tag'

def load_entries(entry_type):
    entries = []
    entry_dir = os.path.join(OUT_DIR, entry_type)
    (_, _, filenames) = os.walk(entry_dir).next()
    for filename in filenames:
        filename = os.path.join(OUT_DIR, entry_type, filename)
        with open(filename) as entry_data:
            entry = jsonpickle.decode(json.load(entry_data))
            entries.append(entry)
            print 'reading in', entry
    return entries

if __name__ == '__main__':
    events = load_entries(EVENT)
    tags = load_entries(TAG)
