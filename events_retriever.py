import contentful
import contentful_datareader
import datetime
import dateutil
from flask import Flask, render_template, request
import os
import pdb
import pytz

from os.path import join, dirname
from dotenv import load_dotenv
try:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except Exception as e:
    print "\nMissing .env file\n"

SPACE_ID = os.environ.get('SPACE_ID', None)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)

# CONTENT_ID_EVENT = 'event'
# CONTENT_ID_TAG = 'tag'

app = Flask(__name__)

@app.route('/')
def index_page():
    events, tags = get_events()
    return render_template('events_tiles.html', events=events, tags=tags)

    # return render_template('events_tiles.html',
    #                 events=contentful_datareader.load_entries(CONTENT_ID_EVENT),
    #                 tags=contentful_datareader.load_entries(CONTENT_ID_TAG))

@app.route('/next2weeks.html')
def next_up():

    def naive(d):
        return d.tzinfo is None or d.tzinfo.utcoffset(d) is None

    events, tags = get_events()

    now = datetime.datetime.now(pytz.utc)
    future_cutoff = now + datetime.timedelta(days=14)


    soon_events = filter(lambda x: x.start_time >= now and x.start_time <= future_cutoff, events)

    return render_template('next2weeks.html', events=soon_events, tags=tags)

def get_events():
    client = contentful.Client(SPACE_ID, ACCESS_TOKEN)
    entries = client.entries()
    events = []
    tags = []
    for entry in entries:

        if(entry.content_type.id == 'event'):
            # standardize contentful's bad timezone handling
            entry.start_time = entry.start_time.replace(tzinfo=pytz.utc)
            events.append(entry)

        if(entry.content_type.id == 'tag'):
            tags.append(entry)

    return sorted(events, key=lambda x: x.start_time.strftime('%Y-%m-%d'), reverse=True), tags

if __name__ == '__main__':
    app.run()
