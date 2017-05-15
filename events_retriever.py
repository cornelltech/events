from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import contentful
import pdb

SPACE_ID = 'g2o2lk221h21'
ACCESS_TOKEN = 'd4d54c120ee06a69e46d8dc64e56e1703093d27524ae6006c8833bc10938ae0f'

app = Flask(__name__)
Bootstrap(app) # why isn't this code doing anything...

@app.route('/')
def index_page():
    return render_template('events_tiles.html', events=get_events())

def get_events():
    client = contentful.Client(SPACE_ID, ACCESS_TOKEN)
    entries = client.entries()
    events = []
    for entry in entries:
        if(entry.content_type.id == 'event'):
            events.append(entry)
    return events

if __name__ == '__main__':
    app.run()
