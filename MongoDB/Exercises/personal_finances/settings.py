from models import category, user

AUTH_FIELD = 'user_id'
DOMAIN = {
    'categories': category.model,
    'users': user.model
}
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
MONGO_DBNAME = 'pf'
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
XML = False