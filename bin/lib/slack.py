#encoding:UTF-8
import json, os, sys, time
from urllib.request import Request, urlopen
from . import log

env_dist = os.environ
slack_url = env_dist.get('SLACK_URL')

def send(msg):
    if slack_url == None:
        log.output("-------Has not config SLACK_URL.-------")
        return
    message = {
        "text": msg
    }
    req = Request(slack_url, json.dumps(message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
    except:
        log.output("slack_msg_send_error: %s" % str(sys.exc_info()))
    