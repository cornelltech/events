from contentful import Client
import datetime
import json
import jsonpickle
import os
import pdb
import pytz
import tzlocal
import os

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

# contentful query
CONTENT_ID_EVENT = 'event'
ORDER_RESULTS_BY = '-sys.updatedAt' # most recently updated first
LIMIT = 3

# config where files get saved
OUT_DIR = 'json'

def process_entries(client):
    skip = 0
    while (True):
        entries = client.entries({
            'order': ORDER_RESULTS_BY,
            'content_type': CONTENT_ID_EVENT,
            'limit': LIMIT,
            'skip': skip})

        for entry in entries:
            filename = OUT_DIR + '/' + entry.sys['id'] + '.json'
            entry_modified = entry.sys['updated_at']
            if (os.path.isfile(filename)):
                file_modified = \
                    datetime.datetime.fromtimestamp(os.path.getmtime(filename),
                                                    tzlocal.get_localzone())

                # if we reach an entry we've already processed, the remaining
                # data on the server is older than our stored data
                if(int((entry_modified - file_modified).total_seconds()) == 0):
                    print 'stopping at: ', entry.event_title, '(', filename, ')'
                    print 'remaining content was processed on an earlier run'
                    return

            with open(filename, 'w') as outfile:
                json.dump(jsonpickle.encode(entry), outfile)
                # TODO: py3 might make these calculations nicer
                contentful_tz = entry_modified.tzinfo
                era_zero = datetime.datetime(1970,1,1).replace(
                                                        tzinfo=contentful_tz)
                in_seconds = (entry_modified - era_zero).total_seconds()
                outfile.close()
                os.utime(filename, (in_seconds, in_seconds))

                print 'saving file: ', entry.event_title, 'id=', entry.sys['id']

        if (len(entries) < LIMIT): # when you reach the final page
            print 'you have processed all the data'
            return
        else:
            skip += LIMIT

if __name__ == '__main__':
    client = Client(SPACE_ID, ACCESS_TOKEN)
    process_entries(client)
