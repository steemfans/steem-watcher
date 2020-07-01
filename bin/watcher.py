#!/usr/bin/python3 -u
#encoding:UTF-8
import json, os, sys, time
from contextlib import suppress
from concurrent import futures
from steem.blockchain import Blockchain
from steem.steemd import Steemd
import traceback
from lib import slack
from lib import db
from lib import opType

env_dist = os.environ

# init block config
print('-------- env params --------')
steemd_url = env_dist.get('STEEMD')
if steemd_url == None or steemd_url == "":
    steemd_url = 'https://api.steemit.com'
print('STEEMD: %s' % steemd_url)

worker_num = env_dist.get('WORKER_NUM')
if worker_num == None or worker_num == "":
    worker_num = 5
print('WORKER_NUM: %s' % (worker_num))
worker_num = int(worker_num)
env_block_num = env_dist.get('BLOCK_NUM')
if env_block_num == None or env_block_num == "":
    start_block_num = 0
else:
    start_block_num = int(env_block_num)
print('BLOCK_NUM: %s' % env_block_num)
print('-------- env params --------')

db_connection = None

# init blockchain
steemd_nodes = [
    steemd_url,
]
s = Steemd(nodes=steemd_nodes)
b = Blockchain(s)

def worker(start, end):
    try:
        global s, b, db_connection
        print('start from {start} to {end}'.format(start=start, end=end))
        # keep log
        with db_connection.cursor() as cursor:
            clear_sql = "DELETE FROM `task_log` WHERE `block_num` >= %s and `block_num` <= %s" % (start, end)
            insert_sql = "INSERT INTO `task_log` (`block_num`, `status`) VALUES "
            data = []
            for i in range(start, end+1):
                data.append("(%s, 0)" % i)
            insert_sql = insert_sql + ','.join(data)
            cursor.execute(clear_sql)
            cursor.execute(insert_sql)
        db_connection.commit()
        # get block
        block_infos = s.get_blocks(range(start, end+1))
        # print(block_infos)
        sql = db.insert_op_sql
        for block_info in block_infos:
            timestamp = int(time.mktime(time.strptime(block_info['timestamp'], "%Y-%m-%dT%H:%M:%S")))
            block_num = block_info['block_num']
            transactions = block_info['transactions']
            for trans in transactions:
                # print(trans)
                operations = trans['operations']
                for op in operations:
                    if op[0] in opType.watchingTypes.keys():
                        with db_connection.cursor() as cursor:
                            cursor.execute(sql % (
                                opType.watchingTypes[op[0]],
                                block_num,
                                trans['transaction_id'],
                                json.dumps(op),
                                timestamp))
                        #db_connection.commit()
        # keep log
        with db_connection.cursor() as cursor:
            sql = "UPDATE `task_log` SET `status` = 1 where `block_num` >= %s and `block_num` <= %s" % (start, end)
            cursor.execute(sql)
        db_connection.commit()
    except:
        print('error: from %s to %s' % (start, end), sys.exc_info())
        #slack.send(':fire: error: from %s to %s' % (start, end))

def get_start_num_from_db():
    global db_connection
    with db_connection.cursor() as cursor:
        sql = "SELECT `block_num` FROM `task_log` ORDER BY `block_num` DESC LIMIT 1"
        cursor.execute(sql)
        log = cursor.fetchone()
        print('start num from db:', log)
    if log == None:
        return 0
    else:
        return int(log['block_num']) + 1

def run():
    global start_block_num, s, b, db_connection

    db.create_db()
    db.create_table()
    db_connection = db.connect_db()

    start_block_num_from_db = get_start_num_from_db()
    if start_block_num_from_db != 0:
        start_block_num = start_block_num_from_db

    while True:
        head_block_number = b.info()['head_block_number']
        end_block_num = int(head_block_number)
        if start_block_num == 0:
            start_block_num = end_block_num - 3
        if start_block_num >= end_block_num:
            continue
        if end_block_num - start_block_num >= 50:
            while start_block_num < end_block_num:
                tmp_end_block_num = start_block_num + 50
                if tmp_end_block_num > end_block_num:
                    tmp_end_block_num = end_block_num
                with futures.ThreadPoolExecutor(max_workers=worker_num) as executor:
                    executor.submit(worker, start_block_num, tmp_end_block_num)
                start_block_num = tmp_end_block_num + 1
        else:
            with futures.ThreadPoolExecutor(max_workers=worker_num) as executor:
                executor.submit(worker, start_block_num, end_block_num)
            start_block_num = end_block_num + 1
        #time.sleep(3)

if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        run()
