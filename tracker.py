from time import sleep
import pymongo
from pymongo import MongoClient
from pymongo.cursor import _QUERY_OPTIONS
from pymongo.errors import AutoReconnect
from bson.timestamp import Timestamp
from pymongo.cursor import CursorType
from sendMail import send_mail

c = pymongo.MongoClient()

# Uncomment this for master/slave.
#oplog = c.local.oplog['$main']
# Uncomment this for replica sets.
oplog = c.local.oplog.rs
first = next(oplog.find().sort('$natural', pymongo.DESCENDING).limit(-1))
ts = first['ts']
# Tailable cursor options.
_TAIL_OPTS = {'tailable': True, 'await_data': True}
# Time to wait for data or connection.
_SLEEP = 1


def notify(table , feild , up):
    print table,feild,up
    db_subs = c.subscriber
    res = db_subs.subscription.find_one({'table':table ,'feild':feild})
    print res['emails']
    msg = up+" on collection "+table+" on field "+feild
    send_mail('DBtracker@mymail.com',res['emails'],'subscribed operation in DB',msg)

def process_operation(doc):
    op  = doc['op']
    table= doc['ns'].split('.')[1]
    feilds = doc['o'].keys()
    obj = doc['o']
    if op == 'i':
        op = 'insert'
    elif op == 'u':
        op = 'update'
    elif op == 'd':
        op ='delete'
    print feilds
    for feild in feilds:
        if feild !='_id':
            notify(table,feild,op)



def tracker():
    db = MongoClient().local
    while True:
        query = {'ts': {'$gt': ts}}  # Replace with your query.
        cursor = db.oplog.rs.find(query, cursor_type=CursorType.TAILABLE_AWAIT, oplog_replay=True)

        cursor.add_option(_QUERY_OPTIONS['oplog_replay'])

        try:
            while cursor.alive:
                try:
                    for doc in cursor:
                        print doc
                        if doc['op']=='n':
                            continue
                        else:
                            process_operation(doc)

                except (AutoReconnect, StopIteration):
                    sleep(_SLEEP)

        finally:
            cursor.close()



if __name__ == '__main__':
  tracker()
