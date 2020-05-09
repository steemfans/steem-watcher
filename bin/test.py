#!/usr/bin/python3 -u
#encoding:UTF-8
import json, os, sys, time
from contextlib import suppress
from lib import slack
from lib import db

def run():
    db_connection = db.connect_db()
    t1 = int(time.mktime(time.strptime("2020-05-04T00:00:00", "%Y-%m-%dT%H:%M:%S")))
    t2 = int(time.mktime(time.strptime("2020-05-05T00:00:00", "%Y-%m-%dT%H:%M:%S")))
    t3 = int(time.mktime(time.strptime("2020-05-06T00:00:00", "%Y-%m-%dT%H:%M:%S")))
    t4 = int(time.mktime(time.strptime("2020-05-07T00:00:00", "%Y-%m-%dT%H:%M:%S")))
    t5 = int(time.mktime(time.strptime("2020-05-08T00:00:00", "%Y-%m-%dT%H:%M:%S")))
    t6 = int(time.mktime(time.strptime("2020-05-09T00:00:00", "%Y-%m-%dT%H:%M:%S")))
    with db_connection.cursor() as cursor:
        sql = db.create_account_from_op_sql
        # op_type: claim_account
        cursor.execute(sql % (t1, t2, 1, '%'+'\"creator\": \"steem\"'+'%'))
        n1 = cursor.fetchone()['num']
        cursor.execute(sql % (t2, t3, 1, '%'+'\"creator\": \"steem\"'+'%'))
        n2 = cursor.fetchone()['num']
        cursor.execute(sql % (t3, t4, 1, '%'+'\"creator\": \"steem\"'+'%'))
        n3 = cursor.fetchone()['num']
        cursor.execute(sql % (t4, t5, 1, '%'+'\"creator\": \"steem\"'+'%'))
        n4 = cursor.fetchone()['num']
        cursor.execute(sql % (t5, t6, 1, '%'+'\"creator\": \"steem\"'+'%'))
        n5 = cursor.fetchone()['num']

    
    msg = ''':evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree:

5月4日 -- 5月8日 @steem账号申请牌子数量统计：

05.04：%s
05.05：%s
05.06：%s
05.07：%s
05.08：%s

'''

    slack.send(msg % (
        n1,
        n2,
        n3,
        n4,
        n5
        ))
    print('send success')
    db_connection.close()

if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        run()