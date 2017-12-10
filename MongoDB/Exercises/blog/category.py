import database as db
from datetime import datetime
from sys import exc_info


def insert_category(name, user):
    print "Inserting category", name

    categories = db.get_categories_collection()

    # Check if category exists
    category_exists = categories.find({'name': name})

    if category_exists.count() > 0:
        print "Category already exists!"
        return False

    try:
        category = {'name': name, 'date': datetime.utcnow(), 'created_by': user}

        result = categories.insert_one(category)
        print "Category inseterd!", result.inserted_id

        return True
    except:
        print "Error inserting category", exc_info()[0]

    return False


def get_categories(include_info=False):
    print "Getting categories"

    categories_collection = db.get_categories_collection()

    cursor = categories_collection.find()
    categories = []

    if include_info:
        for category in cursor:
            categories.append({
                'name': category['name'],
                'date': category['date'].strftime("%A, %B %d %Y at %I:%M%p"),
                'created_by': category['created_by'],
                'posts': 0 # TODO: Count related posts
            })
    else:
        categories = [category['name'] for category in cursor]

    return categories
