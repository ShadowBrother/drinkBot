#!/usr/bin/python
#functions to interact with cocktails.db
#Jesse Hoyt - jesselhoyt@gmail.com


"""list_ingredients
   returns: a list of tuples of ingredients needed to make a drink
   cur(obj) : db cursor object
   drink(string or int) : name of drink or db id of drink
"""
def list_ingredients(cur, drink):
    result = []

    if str(drink).isdigit():#check if drink is int
        
        cur.execute(("SELECT Liquids.name FROM Liquids "
                     "JOIN Mix "
                     "WHERE Mix.drink_id = ? AND Mix.liquid_id == Liquids.id"), (drink,))
    else:#drink is string 
        cur.execute(("SELECT Liquids.name FROM Liquids " 
                     "JOIN Drinks "
                     "JOIN Mix "
                     "WHERE Drinks.name == ? AND Drinks.id == Mix.drink_id AND Liquids.id == Mix.liquid_id"), (drink,))
    for row in cur:#fetch query results and append to a list
        result.append(row)
    return result


"""have_ingredients
   returns(boolean) : True if have all needed ingredients, False if missing any ingredients
   cur(obj) : db cusor object
   drink(string or int) : name of drink or db id of drink
"""
def have_ingredients(cur, drink):
    
    
    
    if str(drink).isdigit():#if drink is int
        cur.execute("SELECT COUNT(*) FROM Mix WHERE drink_id == ? AND NOT EXISTS (SELECT id FROM Inventory WHERE Inventory.liquid_id == Mix.liquid_id)", (drink,))
    else:#drink is string            
        cur.execute("SELECT COUNT(*) FROM Mix WHERE drink_id == (SELECT id FROM Drinks WHERE name == ?) AND NOT EXISTS (SELECT id FROM Inventory WHERE Inventory.liquid_id == Mix.liquid_id)", (drink,))
    missing = cur.fetchone()[0] #untuple it
    
    if missing == 0:
        return True
    else:
        return False

"""have_ingredient
   returns(boolean) : True if have ingredient, False if missing ingredient
   cur(obj) : db cursor object
   ingredient(string or int) : name of ingredient or db id for ingredient
"""
def have_ingredient(cur, ingredient):
    
    if str(ingredient).isdigit():#if drink is int
        cur.execute(("SELECT CASE WHEN EXISTS "
                     "(SELECT * FROM Inventory WHERE liquid_id == ?) "
                     "THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"), (ingredient,))
    else:#drink is string
        cur.execute(("SELECT CASE WHEN EXISTS "
                     "(SELECT Liquids.name FROM Liquids JOIN Inventory "
                     "WHERE Liquids.name == ? AND Liquids.id == Inventory.liquid_id) "
                     "THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"), (ingredient,))
    return cur.fetchone()[0]
    

"""list_recipe
   returns(list of tuples) : a list of tupples of ingredients and amount to make a drink
   cur(obj) : db cursor object
   drink(string or int) : name of drink or db id for drink
"""
def list_recipe(cur, drink):
    result = []
    
    if str(drink).isdigit():#if drink is int
        cur.execute(("SELECT Liquids.name, Mix.Amount "
                     "FROM Liquids JOIN Mix "
                     "WHERE Mix.drink_id == ? AND Liquids.id == Mix.liquid_id"), (drink,))
    else:#drink is string
        cur.execute(("SELECT Liquids.name, Mix.amount "
                     "FROM Liquids JOIN Drinks JOIN MIX "
                     "WHERE Drinks.name ==  ? AND Drinks.id == Mix.drink_id AND Liquids.id == Mix.liquid_id"), (drink,))
    for row in cur:
        result.append(row)
    return result


"""list_all_drinks
   returns(list) : returns list of all drinks
   cur(obj) : db cursor object
"""

def list_all_drinks(cur):
    result = []
    cur.execute("SELECT name FROM Drinks")
    for row in cur:
        result.append(row)
    return result

"""get_drink_id
   returns(int) : id of drink
   cur(obj) : db cursor object
   drink(string) : name of drink
"""
def get_drink_id(cur, drink):
    
    cur.execute("SELECT id FROM Drinks WHERE name == ?", (drink,))
    
    return cur.fetchone()[0]

