#encoding:UTF-8
import json, os, sys, time
import pymysql
from . import log

# init db params
env_dist = os.environ
mysql_host = env_dist.get('MYSQL_HOST')
if mysql_host == None or mysql_host == "":
    mysql_host = '172.22.2.2'
log.output('MYSQL_HOST: %s' % (mysql_host))

mysql_user = env_dist.get('MYSQL_USER')
if mysql_user == None or mysql_user == "":
    mysql_user = 'root'
log.output('MYSQL_USER: %s' % (mysql_user))

mysql_pass = env_dist.get('MYSQL_PASS')
if mysql_pass == None or mysql_pass == "":
    mysql_pass = '123456'
log.output('MYSQL_PASS: %s' % (mysql_pass))

mysql_db = env_dist.get('MYSQL_DB')
if mysql_db == None or mysql_db == "":
    mysql_db = 'watcher'
log.output('MYSQL_DB: %s' % (mysql_db))

insert_op_sql = '''
INSERT INTO `op_log`
    (`op_type`, `block_num`, `tx_id`, `op_data`, `created_at`)
VALUES
    (%s, %s, '%s', '%s', %s)
'''

create_account_from_op_sql = '''
SELECT count(*) as num
FROM `op_log`
WHERE
    created_at >= %s and
    created_at < %s and
    op_type = %s and
    op_data like '%s'
    ;
'''

create_account_from_op_sql2 = '''
SELECT count(*) as num
FROM `op_log`
WHERE
    created_at >= %s and
    created_at < %s and
    op_type = %s
    ;
'''

create_account_order_sql = '''
SELECT
    count(*) as total,
    op_data
FROM
    `op_log`
WHERE
    created_at >= %s and
    created_at <= %s and
    op_type = %s
GROUP BY op_data
ORDER BY total DESC
LIMIT 10;
'''

def connect_db():
    # global mysql_host, mysql_user, mysql_pass
    # Connect to the database
    try:
        log.output('connecting mysql db ......')
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
            log.output('mysql connect error:')
            sys.exit()
    except:
        log.output('mysql is not ready.')
        sys.exit()

def create_db():
    log.output("start creating db")
    try:
        connection = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_pass,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        sql = "CREATE DATABASE %s" % mysql_db;
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
            log.output("Successfully added database")
        except:
            connection.rollback()
            log.output(sys.exc_info())
    except:
        log.output("MYSQL has not been ready.")
        sys.exit()
    finally:
        connection.close()

def create_table():
    log.output("start creating table")
    try:
        connection = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_pass,
            db=mysql_db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        sql1 = '''
        CREATE TABLE `%s`.`op_log` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `op_type` INT NOT NULL,
            `block_num` INT NOT NULL,
            `tx_id` VARCHAR(40) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci' NOT NULL,
            `op_data` TEXT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci' NOT NULL,
            `created_at` INT NOT NULL,
            PRIMARY KEY (`id`),
            INDEX `op_type_index` (`op_type`),
            INDEX `created_at_index` (`created_at`)
        );
        ''' % mysql_db
        sql2 = '''
        CREATE TABLE `%s`.`task_log` (
            `block_num` INT NOT NULL,
            `status` INT NOT NULL,
            PRIMARY KEY (`block_num`)
        );
        ''' % mysql_db
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql1)
                cursor.execute(sql2)
            connection.commit()
            log.output("Successfully added table")
        except:
            connection.rollback()
            log.output(str(sys.exc_info()))
    except:
        log.output("MYSQL has not been ready.")
        sys.exit()
    finally:
        connection.close()
