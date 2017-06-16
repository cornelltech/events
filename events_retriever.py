import contentful
import contentful_datareader
from flask import Flask, render_template, request
import os
import pdb

CONTENT_ID_EVENT = 'event'
CONTENT_ID_TAG = 'tag'

app = Flask(__name__)

@app.route('/')
def index_page():
  return render_template('events_tiles.html',
                    events=contentful_datareader.load_entries(CONTENT_ID_EVENT),
                    tags=contentful_datareader.load_entries(CONTENT_ID_TAG))

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

    return events, tags

if __name__ == '__main__':
    app.run()
