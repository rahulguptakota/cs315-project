#!/usr/bin/env python

import sys; 
sys.path.insert(0, "lib") # this line is necessary for the rest
import os                             # of the imports to work!
import web
import sqlitedb
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

###########################################################################################
##########################DO NOT CHANGE ANYTHING ABOVE THIS LINE!##########################
###########################################################################################

######################BEGIN HELPER METHODS######################

# helper method to convert times from database (which will return a string)
# into datetime objects. This will allow you to compare times correctly (using
# ==, !=, <, >, etc.) instead of lexicographically as strings.

# Sample use:
# current_time = string_to_time(sqlitedb.getTime())

def string_to_time(date_str):
	return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')

# helper method to render a template in the templates/ directory
#
# `template_name': name of template file to render
#
# `**context': a dictionary of variable names mapped to values
# that is passed to Jinja2's templating engine
#
# See curr_time's `GET' method for sample usage
#
# WARNING: DO NOT CHANGE THIS METHOD
def render_template(template_name, **context):
	extensions = context.pop('extensions', [])
	globals = context.pop('globals', {})

	jinja_env = Environment(autoescape=True,
			loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
			extensions=extensions,
			)
	jinja_env.globals.update(globals)

	web.header('Content-Type','text/html; charset=utf-8', unique=True)

	return jinja_env.get_template(template_name).render(context)

#####################END HELPER METHODS#####################

urls = ('/currtime', 'curr_time',
        '/selecttime', 'select_time',
        '/addbids' , 'add_bids',
		'/searchDB' , 'search_DB',
		'/auction_search', 'auction_search',
		# TODO: add additional URLs here
		# first parameter => URL, second parameter => class name
		)
				# '/openbids', 'open_bids',

class auction_search:
	def GET(self):
		return render_template('auction_search.html')

	def POST(self):
		post_params = web.input()
		if post_params['itemId']:
			if post_params['itemId'].isdigit():
				itemId = int(post_params['itemId'])
			else:
				return render_template('auction_search.html', idnotint = "empty")
		else:
			return render_template('auction_search.html', idempty = "empty")		
		itemInfo = sqlitedb.getItem(itemId)
		results = sqlitedb.getItemInfo(itemInfo)
		print results
		return render_template('auction_search.html', result = results )


class search_DB:
	def GET(self):
		return render_template('search_DB.html')

	def POST(self):
		post_params = web.input()
		if (not post_params['itemId']) and (not post_params['category']) and (not post_params['currently']) and (not post_params['description']) and (not post_params['status']):
			return render_template('search_DB.html', message = 'You must fill out atleast one field')
		if post_params['itemId']:
			if post_params['itemId'].isdigit():
				itemId = int(post_params['itemId'])
			else:
				return render_template('search_DB.html', idnotint = "empty")	
		else:
			itemId = ""
		category = post_params['category']
		if post_params['currently']:
			price = "$" + (post_params['currently'])
		else:
			price = ""
		description = post_params['description']
		status = post_params['status']
		kd = {"itemID": itemId, "category": category, "currently": price, "description": description, "status": status}
		result = sqlitedb.searchDB(kd)
		actresult = []
		for thing in result:
			actresult.append(thing)
		print actresult
		if actresult:
			return render_template('search_DB.html', result = actresult)	
		else:
			return render_template('search_DB.html', message = "Result is EMPTY")

class curr_time:
	# A simple GET request, to '/currtime'
	#
	# Notice that we pass in `current_time' to our `render_template' call
	# in order to have its value displayed on the web page
	def GET(self):
		current_time = sqlitedb.getTime()
		newtime = current_time
		return render_template('curr_time.html', msg = newtime)

class select_time:
    # Aanother GET request, this time to the URL '/selecttime'
    def GET(self):
        return render_template('select_time.html')

    # A POST request
    #
    # You can fetch the parameters passed to the URL
    # by calling `web.input()' for **both** POST requests
    # and GET requests
    def POST(self):
        post_params = web.input()
        MM = post_params['MM']
        dd = post_params['dd']
        yyyy = post_params['yyyy']
        HH = post_params['HH']
        mm = post_params['mm']
        ss = post_params['ss']
        enter_name = post_params['entername']


        selected_time = '%s-%s-%s %s:%s:%s' % (yyyy, MM, dd, HH, mm, ss)
        update_message = '(Hello, %s. Previously selected time was: %s.)' % (enter_name, selected_time)
        # TODO: save the selected time as the current time in the database

        # Here, we assign `update_message' to `message', which means
        # we'll refer to it in our template as `message'
        return render_template('select_time.html', message = update_message)

class add_bids:
	def GET(self):
		return render_template('add_bids.html')
	
	def POST(self):
		post_params = web.input()
		itemId = post_params['itemId']
		userId = post_params['userId']
		price = post_params['price']
		currtime = sqlitedb.getTime()
		if (itemId == '') or (price == '') or (userId == ''):
			return render_template('add_bids.html', message = 'You must fill out every field')
		itemId = int(itemId)
		price = float(price)
		user = sqlitedb.getUserById(userId)
		if user == None:
			return render_template('add_bids.html', message = 'User does not exist')

		item = sqlitedb.getItemById(itemId)

		if(item == None):
			return render_template('add_bids.html', message = 'Item does not exists')

		if(item.endTime < currtime):
			return render_template('add_bids.html', message = 'Auction is ended')
		price1=float(item.currently[1:])
		if(price < price1):
			return render_template('add_bids.html', message = 'Please give me higher price')

		if(sqlitedb.addbid(itemId,userId,price,currtime)):
			update_message = "Success"
		else:
			update_message = "Fail"
		return render_template('add_bids.html', message = update_message)

class open_bids:
	def GET(self):
		return render_template('open_bids.html', result = sqlitedb.getOpenAuctions())

###########################################################################################
##########################DO NOT CHANGE ANYTHING BELOW THIS LINE!##########################
###########################################################################################

if __name__ == '__main__':
	print "hi there"
	web.internalerror = web.debugerror
	app = web.application(urls, globals())
	app.add_processor(web.loadhook(sqlitedb.enforceForeignKey))
	sqlitedb.startprocesses()
	app.run()
