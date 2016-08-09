import json
import sys

import requests


# Handles sending messages to webhook
class Output:
    # Webhook's URL taken from program argument
    webhookUrl = str(sys.argv[2])

    # Sends output to webhook
    @classmethod
    def response(cls, text, session_id):
        payload = {'text': text, 'session_id': session_id}
        headers = {'content-type': 'application/json'}
        requests.post(cls.webhookUrl, data=json.dumps(payload), headers=headers)
