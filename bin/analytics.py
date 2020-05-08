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
        sql = '''
            SELECT count(*) as num
            FROM watcher.account_create_log
            WHERE
                op_type = %s and
                creator = '%s' and
                created_at >= %s and
                created_at < %s
                ;
        '''
        # op_type: claim_account
        cursor.execute(sql % (1, 'steem', start_time, now))
        claim_num = cursor.fetchone()['num']

        # op_type: create_claimed_account
        cursor.execute(sql % (2, 'steem', start_time, now))
        claim_account_num = cursor.fetchone()['num']

        # op_type: account_create
        cursor.execute(sql % (3, 'steem', start_time, now))
        account_create_num = cursor.fetchone()['num']

        # get all accounts
        sql = '''
            SELECT count(*) as num
            FROM watcher.account_create_log
            WHERE
                op_type = %s and
                created_at >= %s and
                created_at < %s
                ;
        '''
        # op_type: claim_account
        cursor.execute(sql % (1, start_time, now))
        all_claim_num = cursor.fetchone()['num']

        # op_type: create_claimed_account
        cursor.execute(sql % (2, start_time, now))
        all_claim_account_num = cursor.fetchone()['num']

        # op_type: account_create
        cursor.execute(sql % (3, start_time, now))
        all_account_create_num = cursor.fetchone()['num']

    msg = '''-------------
过去24小时用户注册数量汇总：
<https://steemd.com/@steem|@steem> 申请牌子数量：        %s
<https://steemd.com/@steem|@steem> 使用牌子数量：        %s
<https://steemd.com/@steem|@steem> 使用steem注册用户数量：%s
申请牌子总量：         %s
使用牌子总量：         %s
使用steem注册用户数量： %s
'''

    slack.send(msg % (
        claim_num,
        claim_account_num,
        account_create_num,
        all_claim_num,
        all_claim_account_num,
        all_account_create_num))
    print('send success')
    db_connection.close()

if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        run()