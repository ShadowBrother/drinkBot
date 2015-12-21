import sys
from drinkBot import app
from rq import Queue, Connection, Worker
from drinkBot.dbModels import Drink, Liquid, Mix, Inventory, db, engine
from time import gmtime, strftime

with Connection():
    qs = map(Queue, sys.argv[1:]) or [Queue()]

    w = Worker(qs)
    w.work()
