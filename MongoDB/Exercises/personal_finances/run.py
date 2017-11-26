from eve import Eve

from personal_finances.auth import RolesAuth, add_token

if __name__ == '__main__':
    app = Eve(auth=RolesAuth)
    app.on_insert_accounts += add_token
    app.run()