from eve.auth import TokenAuth
from werkzeug.security import check_password_hash
import random
import string

from personal_finances.run import app

class RolesAuth(TokenAuth):
    def check_auth(self, token,  allowed_roles, resource, method):
        # use Eve's own db driver; no additional connections/resources are used
        accounts = app.data.driver.db['accounts']
        lookup = {'token': token}
        if allowed_roles:
            # only retrieve a user if his roles match ``allowed_roles``
            lookup['roles'] = {'$in': allowed_roles}
        account = accounts.find_one(lookup)
        return account

def add_token(documents):
    # Don't use this in production:
    # You should at least make sure that the token is unique.
    for document in documents:
        document["token"] = (''.join(random.choice(string.ascii_uppercase) for x in range(10)))