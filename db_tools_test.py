#!/usr/bin/python
#script to test function in db_tools.py
#Jesse Hoyt - jesselhoyt@gmail.com

import sqlite3 as lite
import db_tools

con = lite.connect('cocktails.db')

with con:

    cur = con.cursor()

    print db_tools.list_ingredients(cur, 'Gin and Tonic')


    print db_tools.have_ingredients(cur, 'Gin and Tonic')
    print db_tools.have_ingredients(cur, 'Vodka Martini')


    print db_tools.list_recipe(cur, 'Gin and Tonic')
    print
    print db_tools.list_recipe(cur, 'Rum and Coke')


    print
    print db_tools.list_all_drinks(cur)

    print
    print db_tools.have_ingredient(cur, 'Rum')
    print db_tools.have_ingredient(cur, 'Lim Juice')
