#encoding:UTF-8
import json, os, sys, time
from urllib.request import Request, urlopen
from . import log

env_dist = os.environ
analytics_api_url = env_dist.get('ANALYTICS_API')
superkey = env_dist.get('SUPERKEY')
report_url = env_dist.get('REPORT_URL')

def send(event_id, total, date):
    if analytics_api_url == None or analytics_api_url == "":
        log.output("-------Has not config ANALYTICS_API.-------")
        return
    if superkey == None or superkey == "":
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

def report():
    if report_url == None or report_url == "":
        log.output("-------Has not config REPORT_URL.-------")
        return
    try:
        req = Request(report_url)
        response = urlopen(req)
        log.output(response.read())
    except:
        log.output('report_url_msg_send_error: %s' % str(sys.exc_info()))
    finally:
        return
