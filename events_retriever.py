import contentful
import contentful_datareader
from flask import Flask, render_template, request
import os
import pdb

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
    events, tags = get_events()
    return render_template('next2weeks.html', events=events, tags=tags)
    
def get_events():
    client = contentful.Client(SPACE_ID, ACCESS_TOKEN)
    entries = client.entries()
    events = []
    tags = []
    for entry in entries:

        if(entry.content_type.id == 'event'):
            events.append(entry)

        if(entry.content_type.id == 'tag'):
            tags.append(entry)

    return sorted(events, key=lambda x: x.start_time.strftime('%Y-%m-%d'), reverse=True), tags

if __name__ == '__main__':
    app.run()
