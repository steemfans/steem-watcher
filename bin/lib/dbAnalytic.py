#encoding:UTF-8
import json, os, sys, time, re
import pymysql
from . import log
env_dist = os.environ
def connect_db():
    # init db params
    # add DATABASE_URL env support
    database_url = env_dist.get('DATABASE_URL')
    if database_url == None or database_url == "":
        mysql_config = env_dist.get('ANALYTICS_MYSQL_CONFIG')
    else:
        mysql_config = database_url

    if mysql_config == None or mysql_config == "":
        mysql_host = env_dist.get('ANALYTICS_MYSQL_HOST')
        if mysql_host == None or mysql_host == "":
            mysql_host = '172.22.2.2'
        
        mysql_port = env_dist.get('ANALYTICS_MYSQL_PORT')
        if mysql_port == None or mysql_port == "":
            mysql_port = 3306

        mysql_user = env_dist.get('ANALYTICS_MYSQL_USER')
        if mysql_user == None or mysql_user == "":
            mysql_user = 'root'

        mysql_pass = env_dist.get('ANALYTICS_MYSQL_PASS')
        if mysql_pass == None or mysql_pass == "":
            mysql_pass = '123456'

        mysql_db = env_dist.get('ANALYTICS_MYSQL_DB')
        if mysql_db == None or mysql_db == "":
            mysql_db = 'faucet'

    else:
        try:
            matches = re.match(r'mysql://(\S+):(\S+)@(\S+):(\d+)/(\S+)', mysql_config, re.I)
            mysql_host = matches[3]
            mysql_user = matches[1]
            mysql_pass = matches[2]
            mysql_port = int(matches[4])
            mysql_db = matches[5]
        except:
            log.output('ANALYTICS_MYSQL_CONFIG is error.')
            return -1
            #sys.exit()

    log.output('ANALYTICS_MYSQL_HOST: %s' % (mysql_host))
    log.output('ANALYTICS_MYSQL_PORT: %s' % (mysql_port))
    log.output('ANALYTICS_MYSQL_USER: %s' % (mysql_user))
    log.output('ANALYTICS_MYSQL_PASS: %s' % (mysql_pass))
    log.output('ANALYTICS_MYSQL_DB: %s' % (mysql_db))

    mysql_table = env_dist.get('ANALYTICS_MYSQL_TABLE')
    if mysql_table == None or mysql_table == "":
        log.output('need ANALYTICS_MYSQL_TABLE')
        return -1
        #sys.exit()
    log.output('ANALYTICS_MYSQL_TABLE: %s' % (mysql_table))
    # global mysql_host, mysql_user, mysql_pass
    # Connect to the database
    try:
        log.output('connecting analytic mysql db ......')
        conn = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
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
            return -1
            #sys.exit()
    except:
        log.output('analytic mysql is not ready.')
        return -1
        #sys.exit()

def insert_data(db_connection, data):
    if db_connection == -1:
        return -1
    mysql_table = env_dist.get('ANALYTICS_MYSQL_TABLE')
    if mysql_table == None or mysql_table == "":
        log.output('need ANALYTICS_MYSQL_TABLE')
        return -1
        #sys.exit()
    log.output('ANALYTICS_MYSQL_TABLE: %s' % (mysql_table))
    with db_connection.cursor() as cursor:
        insert_sql = "INSERT INTO `%s` (`event_id`, `total`, `created_at`) VALUES " % mysql_table
        insert_sql = insert_sql + ','.join(data)
        cursor.execute(insert_sql)
    db_connection.commit()
    log.output('analytic data insert success.')
