#!/usr/bin/python3 -u
#encoding:UTF-8
import json, os, sys, time
from contextlib import suppress
from lib import slack
from lib import db

def run():
    db_connection = db.connect_db()
    now = int(time.time())
    start_time = now - 24 * 3600
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
        creator = "<https://steemd.com/@%s|@%s>" % (op_detail[1]['creator'], op_detail[1]['creator'])
        order_list.append("%s %s               %s" % (number_icons[i], creator, o['total']))
        i = i + 1

    msg = ''':evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree: :evergreen_tree:
:earth_asia: 过去 24 小时用户注册数量汇总：

<https://steemd.com/@steem|@steem> 申请牌子数量：        %s
<https://steemd.com/@steem|@steem> 使用牌子数量：        %s
<https://steemd.com/@steem|@steem> 使用steem注册用户数量：%s
申请牌子总量：         %s
使用牌子总量：         %s
使用steem注册用户数量： %s

:gem: 过去 24 小时申请牌子排名前 10：

%s
'''

    slack.send(msg % (
        claim_num,
        claim_account_num,
        account_create_num,
        all_claim_num,
        all_claim_account_num,
        all_account_create_num,
        "\n".join(order_list)
        ))
    print('send success')
    db_connection.close()

if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        run()