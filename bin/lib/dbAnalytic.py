#encoding:UTF-8
import json, os, sys, time
import pymysql
from . import log

# init db params
env_dist = os.environ
mysql_host = env_dist.get('ANALYTICS_MYSQL_HOST')
if mysql_host == None or mysql_host == "":
    log.output('need ANALYTICS_MYSQL_HOST')
    sys.exit()
log.output('ANALYTICS_MYSQL_HOST: %s' % (mysql_host))

mysql_user = env_dist.get('ANALYTICS_MYSQL_USER')
if mysql_user == None or mysql_user == "":
    log.output('need ANALYTICS_MYSQL_USER')
    sys.exit()
log.output('ANALYTICS_MYSQL_USER: %s' % (mysql_user))

mysql_pass = env_dist.get('ANALYTICS_MYSQL_PASS')
if mysql_pass == None or mysql_pass == "":
    log.output('need ANALYTICS_MYSQL_PASS')
    sys.exit()
log.output('ANALYTICS_MYSQL_PASS: %s' % (mysql_pass))

mysql_db = env_dist.get('ANALYTICS_MYSQL_DB')
if mysql_db == None or mysql_db == "":
    log.output('need ANALYTICS_MYSQL_DB')
    sys.exit()
log.output('ANALYTICS_MYSQL_DB: %s' % (mysql_db))

mysql_table = env_dist.get('ANALYTICS_MYSQL_TABLE')
if mysql_table == None or mysql_table == "":
    log.output('need ANALYTICS_MYSQL_TABLE')
    sys.exit()
log.output('ANALYTICS_MYSQL_TABLE: %s' % (mysql_table))

def connect_db():
    # global mysql_host, mysql_user, mysql_pass
    # Connect to the database
    try:
        log.output('connecting analytic mysql db ......')
        conn = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_pass,
            db=mysql_db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        if conn.open == True:
            return conn
        else:
            log.output('analytic mysql connect error:')
            sys.exit()
    except:
        log.output('analytic mysql is not ready.')
        sys.exit()

def insert_data(db_connection, data):
    with db_connection.cursor() as cursor:
        insert_sql = "INSERT INTO `%s` (`event_id`, `total`, `created_at`) VALUES " % mysql_table
        insert_sql = insert_sql + ','.join(data)
        cursor.execute(insert_sql)
    db_connection.commit()
    log.output('analytic data insert success.')

    

