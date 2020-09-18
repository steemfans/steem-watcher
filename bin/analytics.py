#!/usr/bin/python3 -u
#encoding:UTF-8
import json, os, sys, time, datetime
from contextlib import suppress
from lib import slack, discord
from lib import api
from lib import db
from lib import dbAnalytic
from lib import log

def run():
    db_connection = db.connect_db()
    analytic_db_connection = dbAnalytic.connect_db()
    today = datetime.date.today()
    timeArray = time.strptime(str(today), "%Y-%m-%d")
    now = int(time.mktime(timeArray))
    start_time = now - 24 * 3600
    start_time_str = datetime.datetime.utcfromtimestamp(start_time).strftime("%Y-%m-%d")
    with db_connection.cursor() as cursor:
        # get steem account
        sql = db.create_account_from_op_sql
        # op_type: claim_account
        cursor.execute(sql % (start_time, now, 1, '%'+'\"creator\": \"steem\"'+'%'))
        claim_num = cursor.fetchone()['num']

        # op_type: create_claimed_account
        cursor.execute(sql % (start_time, now, 2, '%'+'\"creator\": \"steem\"'+'%'))
        claim_account_num = cursor.fetchone()['num']

        # op_type: account_create
        cursor.execute(sql % (start_time, now, 3, '%'+'\"creator\": \"steem\"'+'%'))
        account_create_num = cursor.fetchone()['num']

        # get all accounts
        sql = db.create_account_from_op_sql2
        # op_type: claim_account
        cursor.execute(sql % (start_time, now, 1))
        all_claim_num = cursor.fetchone()['num']

        # op_type: create_claimed_account
        cursor.execute(sql % (start_time, now, 2))
        all_claim_account_num = cursor.fetchone()['num']

        # op_type: account_create
        cursor.execute(sql % (start_time, now, 3))
        all_account_create_num = cursor.fetchone()['num']

        # order accounts
        sql = db.create_account_order_sql
        # op_type: claim_account
        cursor.execute(sql % (start_time, now, 1))
        claim_account_order_list = cursor.fetchall()
    
    number_icons = {
        1: ":one:",
        2: ":two:",
        3: ":three:",
        4: ":four:",
        5: ":five:",
        6: ":six:",
        7: ":seven:",
        8: ":eight:",
        9: ":nine:",
        10: ":keycap_ten:",
    }

    order_list = []
    i = 1
    for o in claim_account_order_list:
        op_detail = json.loads(o['op_data'])
        creator = "@%s" % op_detail[1]['creator']
        order_list.append("%s %s               %s" % (number_icons[i], creator, o['total']))
        i = i + 1

    msg = ''':evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree:
:earth_asia:  Analytics Data for Last 24 Hours：

the `pending claimed accounts` number of @steem created:     %s
the `pending claimed accounts` number of @steem used:        %s
the number of @steem created accounts by spending steem：    %s
the number of `pending claimed accounts` created：           %s
the number of `pending claimed accounts` used:               %s
the number of spending steem to create new account：         %s

:gem: Top 10 in last 24 hours(`pending claimed accounts` created)：

%s
'''

    time_tuple = time.strptime(start_time_str, "%Y-%m-%d")
    created_at = datetime.datetime(
        time_tuple.tm_year,
        time_tuple.tm_mon,
        time_tuple.tm_mday,
        time_tuple.tm_hour,
        time_tuple.tm_min,
        time_tuple.tm_sec)
    dbAnalytic.insert_data(analytic_db_connection ,[
        "(%s, %s, '%s')" % (6, claim_num, created_at),
        "(%s, %s, '%s')" % (7, claim_account_num, created_at),
        "(%s, %s, '%s')" % (8, account_create_num, created_at),
        "(%s, %s, '%s')" % (9, all_claim_num, created_at),
        "(%s, %s, '%s')" % (10, all_claim_account_num, created_at),
        "(%s, %s, '%s')" % (11, all_account_create_num, created_at),
    ])

    # send data to faucet analytics api
    api.send('6', claim_num, start_time_str)
    api.send('7', claim_account_num, start_time_str)
    api.send('8', account_create_num, start_time_str)
    api.send('9', all_claim_num, start_time_str)
    api.send('10', all_claim_account_num, start_time_str)
    api.send('11', all_account_create_num, start_time_str)

    # trigger report action
    api.report()

    # send data to slack
    slack.send(msg % (
        claim_num,
        claim_account_num,
        account_create_num,
        all_claim_num,
        all_claim_account_num,
        all_account_create_num,
        "\n".join(order_list)
        ))
    log.output('send slack success')
    # send data to discord
    discord.send(msg % (
        claim_num,
        claim_account_num,
        account_create_num,
        all_claim_num,
        all_claim_account_num,
        all_account_create_num,
        "\n".join(order_list)
        ))
    log.output('send discord success')
    db_connection.close()
    if analytic_db_connection != -1:
        analytic_db_connection.close()

if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        run()
