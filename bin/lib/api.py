#encoding:UTF-8
import json, os, sys, time
from urllib.request import Request, urlopen
from . import log

env_dist = os.environ
analytics_api_url = env_dist.get('ANALYTICS_API')
superkey = env_dist.get('SUPERKEY')

def send(event_id, total, date):
    if analytics_api_url == None:
        log.output("-------Has not config ANALYTICS_API.-------")
        return
    if superkey == None:
        log.output("-------Has not config SUPERKEY.-------")
        return
    final_url = analytics_api_url + "?event_id=%s&superkey=%s&total=%s&t=%s" % (event_id, superkey, total, date)
    log.output(final_url)
    try:
        req = Request(final_url)
        response = urlopen(req)
        log.output(response.read())
    except:
        log.output('analytics_msg_send_error: %s' % str(sys.exc_info()))
    finally:
        return
