#encoding:UTF-8
import json, os, sys, time
from datetime import datetime

def output(msg):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_txt = json.dumps({"msg": str(msg), "time": now})
    print(log_txt)
