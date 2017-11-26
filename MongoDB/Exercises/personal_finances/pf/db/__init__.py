from pf import app
from flask_pymongo import PyMongo

# Connect to MongoDB and call the connection "pf".
mongo = PyMongo(app)