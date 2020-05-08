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
        CREATE TABLE `watcher`.`account_create_log` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `op_type` INT NOT NULL,
            `block_num` INT NOT NULL,
            `creator` VARCHAR(45) CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci' NOT NULL,
            `original_data` TEXT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_general_ci' NOT NULL,
            `timestamp` INT NOT NULL,
            PRIMARY KEY (`id`),
            INDEX `op_type_index` (`op_type`));
        '''
        sql2 = '''
        CREATE TABLE `watcher`.`task_log` (
            `block_num` INT NOT NULL,
            `status` INT NOT NULL,
            PRIMARY KEY (`block_num`));
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