import contentful
import contentful_datareader
from flask import Flask, render_template, request
import os
import pdb

CONTENT_ID_EVENT = 'event'

app = Flask(__name__)

@app.route('/')
def index_page():
    return render_template('events_tiles.html',
                    events=contentful_datareader.load_entries(CONTENT_ID_EVENT))

if __name__ == '__main__':
    app.run()
