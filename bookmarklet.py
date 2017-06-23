import build_contentful_data
from flask import Flask, request
import os
import requests
from urlparse import urlparse, urljoin

from os.path import join, dirname
from dotenv import load_dotenv

try:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except Exception as e:
    print "\nMissing .env file\n"

EVENTBRITE_OAUTH_TOKEN = os.environ.get('EVENTBRITE_OAUTH_TOKEN', None)

EVENTBRITE_API_BASE = 'https://www.eventbriteapi.com/v3/events/'

app = Flask(__name__)

@app.route("/add/")
def add():
    url = request.args.get('url')
    url_components = urlparse(url)
    if not url_components.netloc == 'www.eventbrite.com':
        return 'This isn\'t an eventbrite page, so we can\'t add it.'

    # hackily parsing eventbrite urls
    event_name = url_components.path.split('/')[-1]
    event_id = event_name.split('-')[-1]
    api_url = urljoin(EVENTBRITE_API_BASE, event_id)
    response = requests.get(
        api_url,
        headers = {
            "Authorization": "Bearer %s" % EVENTBRITE_OAUTH_TOKEN,
        },
        verify = True,
    )
    title = response.json()['name']['text']
    description = response.json()['description']['text']
    startTime = response.json()['start']['local']
    external_url = url

    event_attributes = build_contentful_data.build_event(title,
                                        startTime=startTime,
                                        description=description,
                                        external_url=external_url)
    build_contentful_data.send_event_to_contentful(event_attributes)

    return 'Added to contentful!'

if __name__ == '__main__':
    app.run()
