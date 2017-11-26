from pymongo import MongoClient

CONNECTION = MongoClient('localhost', 27017)
DB = CONNECTION.pymongo

def add_obama():
    people = DB.people

    person = {
        "name": "Barack Obama",
        "role": "President",
        "address": {
            "street": "1600 Pennsylvania Evenue",
            "state": "DC",
            "city": "Washington"
        },
        "interests": [
            "government", "basketball", "the middle east"
        ]
    }

    people.insert(person)

DB.people.find()
