import sys
import logging
import pymysql
import os
import json


#rds settings
username = os.environ['username']
password = os.environ['password']
rds_endpoint = os.environ['rds_endpoint']
db_name = "demo"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

print('user_name is',username)
print('password is',password)
print('rds_endpoint is',rds_endpoint)

print('os.environ')
print(json.dumps(dict(os.environ),indent=4))

try:
    conn = pymysql.connect(rds_endpoint, user=username, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
def handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """

    item_count = 0

    with conn.cursor() as cur:
        cur.execute("create table Employee ( EmpID  int NOT NULL, Name varchar(255) NOT NULL, PRIMARY KEY (EmpID))")
        cur.execute('insert into Employee (EmpID, Name) values(1, "Joe")')
        cur.execute('insert into Employee (EmpID, Name) values(2, "Bob")')
        cur.execute('insert into Employee (EmpID, Name) values(3, "Mary")')
        conn.commit()
        cur.execute("select * from Employee")
        for row in cur:
            item_count += 1
            logger.info(row)
            #print(row)
    conn.commit()

    return "Added %d items from RDS MySQL table" %(item_count)