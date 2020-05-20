#encoding:UTF-8
import json, os, sys, time
from urllib.request import Request, urlopen

env_dist = os.environ
analytics_api_url = env_dist.get('ANALYTICS_API')
superkey = env_dist.get('SUPERKEY')

def send(event_id, total, date):
    if analytics_api_url == None:
        print("\n-------Has not config ANALYTICS_API.-------\n")
        return
    if superkey == None:
        print("\n-------Has not config SUPERKEY.-------\n")
        return
    final_url = analytics_api_url + "?event_id=%s&superkey=%s&total=%s&t=%s" % (event_id, superkey, total, date)
    print(final_url)
    req = Request(final_url)
    try:
        response = urlopen(req)
        print(response.read())
    except:
        print('analytics_msg_send_error:', sys.exc_info())
