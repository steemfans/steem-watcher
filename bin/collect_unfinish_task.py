#!/usr/bin/python3 -u
#encoding:UTF-8
import json, os, sys, time
from contextlib import suppress
from steem.blockchain import Blockchain
from steem.steemd import Steemd
from lib import slack
from lib import db
from lib import opType
import traceback

env_dist = os.environ

# init block config
print('-------- env params --------')
steemd_url = env_dist.get('STEEMD')
if steemd_url == None:
    steemd_url = 'https://api.steemit.com'
print('STEEMD: %s' % steemd_url)
print('-------- env params --------')

db_connection = None

# init blockchain
steemd_nodes = [
    steemd_url,
]
s = Steemd(nodes=steemd_nodes)
b = Blockchain(s)

def worker(block_num_list):
    global s, b, db_connection
    try:
        print('start unfinished block: %s' % json.dumps(block_num_list))
        # get block
        block_infos = s.get_blocks(block_num_list)
        # print(block_infos)
        for block_info in block_infos:
            sql = "INSERT INTO `account_create_log` (`op_type`, `block_num`, `creator`, `original_data`, `created_at`) VALUES (%s, %s, '%s', '%s', %s)"
            timestamp = int(time.mktime(time.strptime(block_info['timestamp'], "%Y-%m-%dT%H:%M:%S")))
            block_num = int(block_info['block_num'])
            transactions = block_info['transactions']
            for trans in transactions:
                operations = trans['operations']
                for op in operations:
                    if op[0] in opType.watchingTypes.keys():
                        with db_connection.cursor() as cursor:
                            cursor.execute(sql % (opType.watchingTypes[op[0]], block_num, op[1]['creator'], json.dumps(op), timestamp))
                        db_connection.commit()
        # keep log
        with db_connection.cursor() as cursor:
            block_num_str = ','.join(str(num) for num in block_num_list)
            sql = "UPDATE `task_log` SET `status` = 1 where `block_num` in (%s)" % block_num_str
            cursor.execute(sql)
        db_connection.commit()
    except:
        print('error: unfinished block: %s' % json.dumps(block_num_list), sys.exc_info())
        traceback.print_exc()

def run():
    global s, b, db_connection

    db_connection = db.connect_db()
    try:
        with db_connection.cursor() as cursor:
            # get lastest block num
            sql = 'SELECT block_num FROM watcher.task_log ORDER BY block_num DESC limit 1'
            cursor.execute(sql)
            lastest_block_num = int(cursor.fetchone()['block_num'])
            # get unfinished tasks
            sql = '''
                SELECT block_num
                FROM watcher.task_log
                WHERE
                    block_num < (%s-500) and
                    status = 0
                ;
            '''
            cursor.execute(sql % lastest_block_num)
            unfinished_tasks = cursor.fetchall()
            if unfinished_tasks == ():
                print('None unfinished tasks')
            else:
                block_num_list = []
                for task in unfinished_tasks:
                    block_num_list.append(task['block_num'])
                # do work
                worker(block_num_list)
    except:
        print('error:', sys.exc_info())
    finally:
        db_connection.close()

if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        run()