import logging
import os
import json

import requests
from flask import Flask, request, make_response
from CommonMark import commonmark

from lib import PushCard, MergeCard, PipelineCard, CommentCard

app = Flask(__name__)
readme = ""
errors = {
        '500': 0,
        '404': 0
        }

@app.route('/')
def root():
    return str(commonmark(readme))

@app.route('/status')
def status():
    return make_response((json.dumps(errors), 200, None))

@app.route('/r/<path:hook>', methods=['POST'])
def redirect_to_office(hook):
    if request.data is None:
        return make_response(('Bad Request', 400, None))
    else:
        card = parse_event(json.loads(request.data))
        resp = requests.post('https://outlook.office.com/{0}'.format(hook), data=json.dumps(card))
        print resp.content
        return make_response(('{0}'.format(resp.content), resp.status_code, None))

@app.errorhandler(404)
def not_found():
    errors['404'] += 1
    return "OK", 404

@app.errorhandler(500)
def internal_error():
    errors['500'] += 1
    return "Problem", 500


def parse_event(payload):
    card = None
    event = payload['object_kind']
    if event == 'push':
        card = PushCard(payload)
    elif event == 'merge_request':
        card = MergeCard(payload)
    elif event == 'pipeline':
        card = PipelineCard(payload)
    elif event == 'note':
        card = CommentCard.get(payload)
    return card.to_dict() if card is not None else None

# {
#   title:
#   text: Markdown
#   potentialAction: {
#       @context:
#       @type:
#       name:
#       target:
#   }
# }
# {\"title\": \"Learn about Office 365 Connectors\", \"text\": \"Visit the [Outlook Dev Portal](https://dev.outlook.com) to learn more about Office 365 Connectors!\", \"themeColor\": \"EA4300\", \"potentialAction\": [{\"@context\": \"https://schema.org\", \"@type\": \"ViewAction\", \"name\": \"Open Outlook Dev Center\", \"target\": [\"https://dev.outlook.com\"]}]}" <YOUR WEBHOOK URL>


if __name__ == '__main__':
    readme = str(open('ReadMe.md', 'r').read())
#    logging.basicConfig(level=logging.INFO)
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
