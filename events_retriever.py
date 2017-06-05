import contentful
from flask import Flask, render_template, request
import pdb
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

app = Flask(__name__)

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
