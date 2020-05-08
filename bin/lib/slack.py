#encoding:UTF-8
import json, os, sys, time
from urllib.request import Request, urlopen

env_dist = os.environ
slack_url = env_dist.get('SLACK_URL')

def send(msg):
    if slack_url == None:
        print("\n-------Has not config SLACK_URL.-------\n")
        return
    message = {
        "text": msg
    }
    req = Request(slack_url, json.dumps(message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
    except:
        print('slack_msg_send_error:', sys.exc_info())
    