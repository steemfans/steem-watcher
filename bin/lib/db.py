#encoding:UTF-8
import json, os, sys, time
import pymysql

# init db params
env_dist = os.environ
mysql_host = env_dist.get('MYSQL_HOST')
if mysql_host == None:
    mysql_host = '172.22.2.2'
print('MYSQL_HOST: %s' % (mysql_host))

mysql_user = env_dist.get('MYSQL_USER')
if mysql_user == None:
    mysql_user = 'root'
print('MYSQL_USER: %s' % (mysql_user))

mysql_pass = env_dist.get('MYSQL_PASS')
if mysql_pass == None:
    mysql_pass = '123456'
print('MYSQL_PASS: %s' % (mysql_pass))

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
    watcher.op_log
WHERE
    created_at >= %s and
    created_at <= %s and
    op_type = %s
GROUP BY op_data
ORDER BY total DESC
LIMIT 5;
'''

def connect_db():
    # global mysql_host, mysql_user, mysql_pass
    # Connect to the database
    try:
        print('connecting mysql db ......')
        conn = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_pass,
            db='watcher',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        if conn.open == True:
            return conn
        else:
            print('mysql connect error:')
            sys.exit()
    except:
        print('mysql is not ready.')
        sys.exit()

def create_db():
    print("start creating db")
    try:
        connection = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_pass,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        sql = "CREATE DATABASE watcher";
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
            print("Successfully added database")
        except:
            connection.rollback()
            print(sys.exc_info())
    except:
        print("MYSQL has not been ready.")
        sys.exit()
    finally:
        connection.close()

def create_table():
    print("start creating table")
    try:
        connection = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_pass,
            db='watcher',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        sql1 = '''
        CREATE TABLE `watcher`.`op_log` (
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
        '''
        sql2 = '''
        CREATE TABLE `watcher`.`task_log` (
            `block_num` INT NOT NULL,
            `status` INT NOT NULL,
            PRIMARY KEY (`block_num`)
        );
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql1)
                cursor.execute(sql2)
            connection.commit()
            print("Successfully added table")
        except:
            connection.rollback()
            print(sys.exc_info())
    except:
        print("MYSQL has not been ready.")
        sys.exit()
    finally:
        connection.close()