from pymongo import MongoClient

def connect_db():
    connection = MongoClient('localhost', 27017)
    db = connection.blog
    return db

def get_posts_collection():
    db = connect_db()
    return db.posts

def get_users_collection():
    db = connect_db()
    return db.users

def get_user_sessions_collection():
    db = connect_db()
    return db.user_sessions