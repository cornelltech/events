from contentful import Client
import json
import jsonpickle
import os
import pdb
import shutil

from os.path import join, dirname
from dotenv import load_dotenv

try:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except Exception as e:
    print "\nMissing .env file\n"

# contentful space data
SPACE_ID = os.environ.get('SPACE_ID', None)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)

# contentful query data
CONTENT_ID_EVENT = 'event'
CONTENT_ID_TAG = 'tag'
LIMIT = 100

# config where files get saved
OUT_DIR = 'data'

def process_entries(client, entry_type):
    skip = 0
    entry_dir = os.path.join(OUT_DIR, entry_type)

    if (os.path.exists(entry_dir)): # remove old version of entries
        shutil.rmtree(entry_dir)
    os.makedirs(entry_dir)
    while (True):
        entries = client.entries({
            'content_type': entry_type,
            'limit': LIMIT,
            'skip': skip})

        for entry in entries:
            filename = os.path.join(entry_dir, entry.sys['id'] + '.json')
            with open(filename, 'w') as outfile:
                json.dump(jsonpickle.encode(entry), outfile)
                print 'saving', entry_type, entry.sys['id']

        if (len(entries) < LIMIT): # when you reach the final page
            print 'you have processed all the data of type: ', entry_type
            return
        else:
            skip += LIMIT

if __name__ == '__main__':
    client = Client(SPACE_ID, ACCESS_TOKEN)
    if (not os.path.exists(OUT_DIR)):
        os.makedirs(OUT_DIR)
    process_entries(client, CONTENT_ID_EVENT)
    process_entries(client, CONTENT_ID_TAG)
