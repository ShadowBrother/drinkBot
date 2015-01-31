#!/usr/bin/python
#creates tables for cocktails.db
#Jesse Hoyt - jesselhoyt@gmail.com

#update - 7/10/14 - added foreign keys to mix table
import sqlite3 as lite
import sys


#lists of value tuples for easy insertion into tables
liquids = [('Gin',), ('Rum',), ('Vodka',), ('Jack Daniels',), ('Coke',), ('Vermouth',), ('Tonic',), ("Lime Juice",)]

drinks = [('Gin and Tonic', 3.00), ('Jack and Coke', 3.00), ('Rum and Coke', 3.50), ('Vodka Martini', 5.00)]

inventory = [('Gin',), ('Tonic',), ('Jack Daniels',), ('Coke',), ('Vodka',)]

mix = [('Gin and Tonic', 'Gin', 1), ('Gin and Tonic', 'Tonic', 1), ('Jack and Coke', 'Jack Daniels', 1), ('Jack and Coke', 'Coke',\
3), ('Rum and Coke', 'Rum', 5), ('Rum and Coke', 'Coke', 12), ('Rum and Coke', 'Lime Juice', 1), ('Vodka Martini', 'Vodka', \
2), ('Vodka Martini', 'Vermouth', 1)] 


con = lite.connect('cocktails.db')

with con:
    

    cur = con.cursor()

    #drop tables if they exist
    cur.execute("DROP TABLE IF EXISTS Liquids")
    cur.execute("DROP TABLE IF EXISTS Drinks")
    cur.execute("DROP TABLE IF EXISTS Inventory")
    cur.execute("DROP TABLE IF EXISTS Mix")

    #create Liquids table and insert values
    cur.execute("CREATE TABLE Liquids(id INTEGER PRIMARY KEY, name TEXT)")
    cur.executemany("INSERT INTO Liquids(name) VALUES(?)", liquids)
    con.commit()

    cur.execute("SELECT * FROM Liquids")
    for row in cur:
        print row

    #create Drinks table and insert values
    cur.execute("CREATE TABLE Drinks(id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    cur.executemany("INSERT INTO Drinks(name, price) VALUES(?, ?)", drinks)
    con.commit()

    cur.execute("SELECT * FROM Drinks")
    for row in cur:
        print row

    

    #get liquid_ids from Liquids table to insert into Inventory table
    inventory_ids = []
    for liquid in inventory:
        cur.execute("SELECT id FROM Liquids WHERE name == ?", liquid)
        liq_id = cur.fetchone() 
        inventory_ids.append(liq_id)

        
    for inv_id in inventory_ids:
        print inv_id

    #create Inventory table and insert values
    cur.execute("CREATE TABLE Inventory(id INTEGER PRIMARY KEY, liquid_id INTEGER, FOREIGN KEY(liquid_id) REFERENCES liquid(id))")
    cur.executemany("INSERT INTO Inventory(liquid_id) VALUES(?)", inventory_ids)
    con.commit()

    cur.execute("SELECT * FROM Inventory")
    for row in cur:
        print row


    
    
    #create Mix table and insert values
    cur.execute("CREATE TABLE Mix(id INTEGER PRIMARY KEY, drink_id INTEGER, liquid_id INTEGER, amount INTEGER, FOREIGN KEY(drink_id) REFERENCES drink(id), FOREIGN KEY(liquid_id) REFERENCES liquid(id))")

    #loop through mix list and look up ids in appropriate tables
    for i in mix:
        print i[0]
        cur.execute("SELECT id FROM Drinks WHERE name == ?", (i[0],))
        drink_id = cur.fetchone()
        cur.execute("SELECT id FROM Liquids WHERE name == ?", (i[1],))
        liq_id = cur.fetchone()
        cur.execute("INSERT INTO Mix(drink_id, liquid_id, amount) VALUES(?,?,?)", (drink_id[0], liq_id[0], i[2]))#indexes required since they are tuples

    con.commit()

    cur.execute("SELECT * FROM Mix")
    for row in cur:
        print row
