# -*- coding: utf-8 -*-

import contentful
import contentful_datareader

from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import sys

from os.path import join, dirname
from dotenv import load_dotenv
try:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except Exception as e:
    print "\nMissing .env file\n"
    sys.exit(-1)

SPACE_ID = os.environ.get('SPACE_ID', None)
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', None)
TEMPLATES_DIR = 'templates'

def get_events_and_tags():
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

# The current template relies on Flask. This is a workaround to fix it.
# TODO: remove url_for from the template file.
def url_for(dir, filename=""):
    return "/".join((dir, filename))

if __name__ == '__main__':
    # We fetch the data from Contentful, both events and tags.
    (events, tags) = get_events_and_tags()

    # We load the jinja2 environment, including path and new functions.
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), extensions=['jinja2.ext.with_'])
    env.globals['url_for'] = url_for
    
    # We render the template
    template = env.get_template('events_tiles.html')
    html = template.render({'events': events, 'tags': tags})
    print(html)
    