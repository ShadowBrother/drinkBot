#!/usr/local/bin/python

import sqlite3 as lite
import db_tools

con = lite.connect('cocktails.db')

with con:
	cur = con.cursor()

	print "Content-Type: text/html"
	print

	print """
	<html>
	<head>
		<title>DrinkBot</title>
		<meta charset="utf-8"/>
		<link rel="stylesheet" href="drinkBot.css"/>
		<script src="/resources/jquery-1.11.1.min.js"></script>
		<script src="/resources/jquery-ui-1.10.4.custom.min.js"></script>
		<script src="drinkBot.js"></script>
	</head>
	<body>
		<h1>Drink Menu</h1>
		<div id="drinks">"""

	drinks = db_tools.list_all_drinks(cur)
	for drink in drinks:
		print """<h3 class="drink">""" + drink[0]
		have_ingredients = db_tools.have_ingredients(cur, drink[0])
		if not (have_ingredients):
			print """ - <span class="unavailable">Currently Unavailable</span>"""
		ingredients = db_tools.list_recipe(cur, drink[0])
		print """</h3><div class="ingredients"><ul>"""
		for ing in ingredients:
			print """<li>""" + str(ing[1]) + """ part/s """ + ing[0]
			if (not have_ingredients) and (not db_tools.have_ingredient(cur, ing[0])):
				print """ - <span class="unavailable">currently unavailable</span>"""
			print """</li>"""
		print """</ul></div>"""	
		
		
	print """</div>
	</body>
	</html>"""