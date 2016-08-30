from wit import Wit
from config import config

access_token = config["wit_token"]

actions = {}

client = Wit(access_token, actions)


def get_entities(text):
    resp = client.message(text)
    ent_out = {}
    for key in resp['entities']:
        if resp['entities'][key][0]['confidence'] > 0:
            ent_out.update({key: resp['entities'][key][0]['value']})

    intent = resp.get('intent', False)
    if intent:
        if intent[0]['confidence'] > 0:
            ent_out.update({'intent': intent[0]['value']})
    return ent_out


