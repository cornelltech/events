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

SPACE_ID = os.environ.get('SPACE_ID', None)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
CONTENT_ID_EVENT = 'event'
ORDER_RESULTS_BY = '-sys.updatedAt' # most recently updated first
LIMIT = 3



client = Client(SPACE_ID, ACCESS_TOKEN)

entries = client.entries({'order': ORDER_RESULTS_BY, 'content_type': CONTENT_ID_EVENT})

for entry in entries:
    filename = 'json/' + entry.sys['id'] + '.json'
    entry_modified = entry.sys['updated_at']
    if (os.path.isfile(filename)):
        file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filename), tzlocal.get_localzone())
        if(int((entry_modified - file_modified).total_seconds()) == 0):
            print 'actually you have read all this stuff already'
            break

    print entry.event_title
    print entry.sys['id']

    with open(filename, 'w') as outfile:
        json.dump(jsonpickle.encode(entry), outfile)
        # this is really hacky #woohoo
        contentful_tz = entry_modified.tzinfo
        era_zero = datetime.datetime(1970,1,1).replace(tzinfo=contentful_tz)
        in_seconds = (entry_modified - era_zero).total_seconds()
        outfile.close()
        os.utime(filename, (in_seconds, in_seconds))
