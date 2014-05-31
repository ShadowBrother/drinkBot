#!/usr/bin/python
#script to test function in db_tools.py
#Jesse Hoyt - jesselhoyt@gmail.com

import sqlite3 as lite
import db_tools
import time

con = lite.connect('cocktails.db')

with con:

    cur = con.cursor()
    
    start = time.time()
    print db_tools.list_ingredients(cur, 'Gin and Tonic')
    print str(time.time() - start)
    start = time.time()
    print db_tools.list_ingredients(cur, 1)
    print str(time.time() - start)

    start = time.time()
    print "have ingredients Gin and Tonic? " + str(db_tools.have_ingredients(cur, 'Gin and Tonic'))
    print str(time.time() - start)
    start = time.time()
    print "have ingredients Vodka Martini? " + str(db_tools.have_ingredients(cur, 'Vodka Martini'))
    print str(time.time() - start)
    start = time.time()
    print "have ingredients Rum and Coke? " + str(db_tools.have_ingredients(cur, 'Rum and Coke'))
    print str(time.time() - start)
    start = time.time()
    print db_tools.have_ingredients(cur, 1)
    print str(time.time() - start)
    start = time.time()
    print db_tools.have_ingredients(cur, 3)
    print str(time.time() - start)
    start = time.time()
    print db_tools.list_recipe(cur, 'Gin and Tonic')
    print str(time.time() - start)
    print
    start = time.time()
    print db_tools.list_recipe(cur, 'Rum and Coke')
    print str(time.time() - start)
    print
    start = time.time()
    print db_tools.list_recipe(cur, 2)
    print str(time.time() - start)
    start = time.time()
    print db_tools.list_recipe(cur, 3)
    print str(time.time() - start)
    print
    start = time.time()
    print db_tools.list_all_drinks(cur)
    print str(time.time() - start)
    
    print
    print "have rum? " + str(db_tools.have_ingredient(cur, 'Rum'))
    print "have Lime Juice? " + str(db_tools.have_ingredient(cur, 'Lime Juice'))
    print "have Vodka? " + str(db_tools.have_ingredient(cur, 'Vodka'))

    print
    print "Vodka Martini has id: " + str(db_tools.get_drink_id(cur, 'Vodka Martini'))
    print "Rum and Coke has id: " + str(db_tools.get_drink_id(cur, 'Rum and Coke'))
