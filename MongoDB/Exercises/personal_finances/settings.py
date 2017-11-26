from models import category

DOMAIN = {
    'category': category.model
}
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
MONGO_DBNAME = 'pf'
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
XML = False