import web
import threading
import time
db = web.database(dbn='sqlite',
        db='auction.db' #TODO: add your SQLite database filename
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except:
#     t.rollback()
#     raise
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select currtime from TIME'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    # print results[0]['currtime'], " i am getTime"
    return int(results[0]['currtime']) # TODO: update this as well to match the
                                  # column name

# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from Items where item_ID = $itemID'
    result = query(query_string, {'itemID': item_id})
    return result[0]

# helper method to determine whether query result is empty
# Sample use:
# query_result = sqlitedb.query('select currenttime from Time')
# if (sqlitedb.isResultEmpty(query_result)):
#   print 'No results found'
# else:
#   .....
#
# NOTE: this will consume the first row in the table of results,
# which means that data will no longer be available to you.
# You must re-query in order to retrieve the full table of results
def isResultEmpty(result):
    try:
        result[0]
        return False
    except:
        return True

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return db.query(query_string, vars)

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time

def getOpenAuctions():
    query_string = "select * from ITEMS where startTime > "+ str(1)+" AND endTime < "+ str(getTime())
    result = query(query_string)
    print result[0]
    return result

def getClosedAuctions():
    query_string = "select * from ITEMS where endTime < "+ str(getTime())
    result = query(query_string)
    return result

def startprocesses():
    start()

def start():
    print "hello"
    query_string = "delete from TIME"
    query(query_string)
    query_string = " insert into TIME values (1)"#+ int(time.time())
    query(query_string)
    starttiming()

def starttiming():
    print "hello"
    threading.Timer(1.0, starttiming).start()
    query_string = "update TIME set currtime = " + str(int(time.time()))
    query(query_string)
    print query_string, "this is query string"

def addbid(itemId,userId,price,currtime):
    if db.insert('BID',  itemID=itemId,userID=userId,bidtime=currtime,bidmoney=price):
        return True
    else:
        return False
