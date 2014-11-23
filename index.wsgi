

import sqlite3 as lite

import sys
import os
sys.path.append(os.path.dirname("/var/www/drinkBot/db_tools.py"))
from db_tools import *

#application object, mod_wsgi expects it to be named 'application'
def application(environ, start_response):
	#environ points to dictionary containing CGI like variables
	#which is filled by the server fo reach recvieved request from client

	#start_response is callback function supplied by server


	con = lite.connect('/var/www/drinkBot/drinkBot/cocktails.db')#connect to db

	with con:#with serves as basic try, except, finally block
		cur = con.cursor()#cur is what we use to query db
		
		#create list of strings that we'll turn into output string
		#start by creating basic HTML structure and includes
		return_lst = [ """
	<html>
	<head>
		<title>DrinkBot</title>
		<meta charset="utf-8"/>
		<link rel="stylesheet" href="../../drinkBot/drinkBot/static/drinkBot.css"/>
		<script src="../../resources/jquery-1.11.1.min.js"></script>
		<script src="../../resources/jquery-ui-1.10.4.custom.min.js"></script>
		<script src="../../drinkBot/drinkBot/static/drinkBot.js"></script>
	</head>
	<body>
		<h1>Drink Menu</h1>
		<div id="drinks">"""]
		#query for list of all drinks
		drinks = list_all_drinks(cur)
		#iterate through drinks and create header for drink name
		for drink in drinks:
			return_lst.append( """<h3 class="drink">""")
			return_lst.append(str(drink[0]))
			#query to check inventory for needed drink ingredients
			have_ing = have_ingredients(cur, drink[0])
			if not (have_ing):#if missing ingredients, display that info
				return_lst.append( """ - <span class="unavailable">Currently Unavailable</span>""")
			#query for recipe and create HTML to display it
			ingredients = list_recipe(cur, drink[0])
			return_lst.append( """</h3><div class="ingredients"><ul>""")
			for ing in ingredients:#iterate ingredients appending to return_lst
				return_lst.append("""<li>""" + str(ing[1]) + """ part/s """)
				return_lst.append(str(ing[0]))
				if (not have_ing) and (not have_ingredient(cur, ing[0])):#if missing ingredient
					return_lst.append(""" - <span class="unavailable">currently unavailable</span>""")
				return_lst.append( """</li>""")
			return_lst.append( """</ul></div>""")	
		return_lst.append( """</div>
	</body>
	</html>""")

	status = '200 OK'#HTTP response code and message
	output = ''.join(return_lst)#creates single string from list of strings

	#HTTP headers
	#Must be a list of tupled pairs
	response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(output)))]

	start_response(status, response_headers)#send to server

	#output = str(sys.executable)
	return [output]#output should be iteratable of strings
