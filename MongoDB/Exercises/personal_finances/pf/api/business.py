from sys import exc_info

from pf.db.models import Category

def get_all_categories(where=None):
    if where:
        return
    else:
        return Category.objects.all()

def create_category(data):
    try:
        id = data.get('id')
        name = data.get('name')

        result = Category(name=name, id=id).save()
        print(dumps(result))
        return result
    except:
        print "Unexpected error:", exc_info()[0]
        raise
