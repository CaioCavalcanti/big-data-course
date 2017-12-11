import database as db
from datetime import datetime
from sys import exc_info
from re import compile


def insert_category(name, user):
    print "Inserting category", name

    categories = db.get_categories_collection()

    # Check if category exists
    category_exists = categories.find({'name': name})

    if category_exists.count() > 0:
        print "Category already exists!"
        return False

    try:
        # Combine everything that isn't alphanumeric
        exp = compile('\W')
        whitespace = compile('\s')
        category_id = exp.sub('', whitespace.sub('_', name))

        category = {'_id': category_id, 'name': name,
                    'date': datetime.utcnow(), 'created_by': user}

        result = categories.insert_one(category)
        print "Category inseterd!", result.inserted_id

        return True
    except:
        print "Error inserting category", exc_info()[0]

    return False


def get_category_by_id(id):
    categories_collection = db.get_categories_collection()

    category = categories_collection.find_one({'_id': id})

    return category


def get_category_options():
    print "Gettings category options"

    categories_collection = db.get_categories_collection()

    cursor = categories_collection.find()

    return [{'id': category['_id'], 'name': category['name']} for category in cursor]


def get_categories(include_info=False):
    print "Getting categories"

    categories_collection = db.get_categories_collection()

    cursor = categories_collection.find()
    categories = []

    if include_info:
        posts_collection = db.get_posts_collection()

        for category in cursor:
            posts_count = posts_collection.find({'category_id': category['_id']}).count()

            categories.append({
                'id': category['_id'],
                'name': category['name'],
                'date': category['date'].strftime("%A, %B %d %Y at %I:%M%p"),
                'created_by': category['created_by'],
                'posts': posts_count
            })
    else:
        categories = [category['name'] for category in cursor]

    return categories
