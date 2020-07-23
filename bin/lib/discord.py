#encoding:UTF-8
import json, os, sys, time
from urllib.request import Request, urlopen
from . import log

env_dist = os.environ
discord_url = env_dist.get('DISCORD_URL')

def send(msg):
    if discord_url == None or discord_url == "":
        log.output("-------Has not config DISCORD_URL.-------")
        return
    message = {
        "content": msg
    }
    req = Request(discord_url, json.dumps(message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
    except:
        log.output("discord_url_send_error: %s" % str(sys.exc_info()))
    