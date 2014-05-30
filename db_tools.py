#!/usr/bin/python
#functions to interact with cocktails.db
#Jesse Hoyt - jesselhoyt@gmail.com


"""list_ingredients
   returns: a list of tuples of ingredients needed to make a drink
   cur(obj) : db cursor object
   drink_name(string) : name of drink
"""
def list_ingredients(cur, drink_name):
    result = []
    cur.execute(("SELECT Liquids.name FROM Liquids " 
    "JOIN Drinks "
    "JOIN Mix "
    "WHERE Drinks.name == ? AND Drinks.id == Mix.drink_id AND Liquids.id == Mix.liquid_id"), (drink_name,))
    for row in cur:
        result.append(row)
    return result


"""have_ingredients
   returns(boolean) : True if have all needed ingredients, False if missing any ingredients
   cur(obj) : db cusor object
   drink_name(string) : name of drink
"""
def have_ingredients(cur, drink_name):
    
    #print drink_name
    
    
    cur.execute("SELECT COUNT(*) FROM Mix WHERE drink_id == (SELECT id FROM Drinks WHERE name == ?) AND NOT EXISTS (SELECT id FROM Inventory WHERE Inventory.liquid_id == Mix.liquid_id)", (drink_name,))
    missing = cur.fetchone()[0] #untuple it
    #print missing
    if missing == 0:
        return True
    else:
        return False

"""have_ingredient
   returns(boolean) : True if have ingredient, False if missing ingredient
   cur(obj) : db cursor object
   ingredient_name(string) : name of ingredient
"""
def have_ingredient(cur, ingredient_name):
    
    cur.execute(("SELECT CASE WHEN EXISTS "
                 "(SELECT Liquids.name FROM Liquids JOIN Inventory WHERE Liquids.name == ? AND Liquids.id == Inventory.id) "
                 "THEN CAST(1 AS BIT) ELSE CAST(0 AS BIT) END"), (ingredient_name,))
    return cur.fetchone()[0]
    

"""list_recipe
   returns(list of tuples) : a list of tupples of ingredients and amount to make a drink
   cur(obj) : db cursor object
   drink_name(string) : name of drink
"""
def list_recipe(cur, drink_name):
    result = []
    cur.execute(("SELECT Liquids.name, Mix.amount "
                 "FROM Liquids JOIN Drinks JOIN MIX "
                 "WHERE Drinks.name ==  ? AND Drinks.id == Mix.drink_id AND Liquids.id == Mix.liquid_id"), (drink_name,))
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



