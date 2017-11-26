from pf.db import db

def get_categories():
    return db.categories.find()
    
def create_category(category):
    db.categories.save(category)