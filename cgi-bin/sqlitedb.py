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
    query_string = 'select * from ITEMS where itemID = $itemID'
    result = query(query_string, {'itemID': item_id})
    return result[0]


def getUserById(user_id):
    query_string = 'select * from USER where userID = $userID'
    result = query(query_string, {'userID': user_id})
    return result[0]

def searchDB(kd):
	def getStatusString(status):
		if status == "open":
			return "I.startTime <= $time AND I.endTime > $time"
		elif status == "close":
			return "I.endTime <= $time"
		elif status == "notStarted":
			return "I.startTime > $time"
		else:
			return "1 = 1"
	keys = ["itemID","category","currently","description","status"]        
	query_string = "SELECT * FROM ITEMS I, CATEGORY C WHERE "
	conjunction = []
	itemID = "I.itemID = $itemID"
	category = "C.name = $category AND I.itemID = C.itemID"
	currently = "I.currently = $currently"
	status = getStatusString(kd['status'])
	description = "I.description LIKE $description"
	print kd
	if "description" in kd:
		kd["description"] = "%"+kd["description"]+"%"
	if not kd["itemID"]:
		itemID = "1=1"
	if not kd["category"]:
		category = "1=1"
	if not kd["currently"]:
		currently = "1=1"
	if not kd["status"]:
		status = "1=1"	
	if not kd["description"]:
		description = "1=1"				
	for key in keys:
		if key in kd:
			conjunction.append(locals()[key]) 
	predicate = " AND ".join(conjunction)
	query_string = query_string + predicate
	print query_string
	print kd , "this is kd form data"
	result = query(query_string,{"itemID": kd["itemID"],"category": kd["category"],"currently": kd["currently"],"description": kd["description"],"time": getTime()})
	actresult = []
	for thing in result:
		actresult.append(thing)
	print actresult
	return [actresult[0]]

def getItem(item):
	query_string = "SELECT itemID, startTime, endTime FROM ITEMS WHERE itemID=$itemID"
	results = query(query_string,{"itemID": item})
	# print results[0]
	return results[0]

def getItemInfo(item):
	# t = transaction()
	# try:
	status = "Open"
	if getTime() < item["startTime"]:
		status = "Not Started"
	if getTime() > item["endTime"]:
		status = "Closed"
	query_string = "SELECT * FROM BID WHERE itemID = $itemID ORDER BY bidmoney DESC"
	bids = query(query_string,{"itemID": item["itemID"]})
	bidlist = []
	for bid in bids:
		print bid
		bidlist.append(bid)
	# print bidlist
	winner = "There is no winner"
	if len(bidlist) > 0 and status == "Closed":
		winner = bidlist[0]["userID"]
	# except Exception as e:
	# 	print "\n\n here \n \n "
	# 	t.rollback()
	# 	return (str(e),"","")
	# else:
	# 	t.commit()
	resultdict = {}
	resultdict['status'] = status
	resultdict['winner'] = winner
	resultdict['bidlist'] = bidlist
	print resultdict
	return resultdict	


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
	query_string = " insert into TIME values ("+str(int(time.time()))+")"
	query(query_string)
	starttiming()

def starttiming():
	print "hello"
	threading.Timer(1.0, starttiming).start()
	query_string = "update TIME set currtime = currtime + 1"
	query(query_string)
	print query_string, "this is query string"

def addbid(itemId,userId,price,currtime):
	if db.insert('BID',  itemID=itemId,userID=userId,bidtime=currtime,bidmoney=price):
		return True
	else:
		return False
