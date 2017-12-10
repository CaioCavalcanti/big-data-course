import re
from random import choice
from hashlib import sha256
import pymongo
import bson
from string import ascii_letters
from sys import exc_info
import hmac

import database as db

# Secret for hashing passwords
SECRET = "YourVerySecretPhrase"

def validate_signup(email, password, errors):
    PASS_RE = re.compile(r"^.{3,20}$") 
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    if not PASS_RE.match(password): 
        errors['password_error'] = "invalid password." 
        return False

    if email:
        if not EMAIL_RE.match(email): 
            errors['email_error'] = "invalid email address" 
            return False 
        return True 

def validate_login(email, password):
    users = db.get_users_collection()

    try:
        user = users.find_one({'_id': email})
    except:
        print "User doesnt exist"
        return False

    salt = user['password'].split(',')[1]

    if user['password'] != make_pw_hash(password, salt):
        print "Incorrect password"
        return False

    return True

def newuser(email, password): 
    password_hash = make_pw_hash(password) 

    user = {'_id': email, 'password': password_hash}

    users = db.get_users_collection()

    try: 
        users.insert(user)
    except pymongo.errors.DuplicateKeyError as e: 
        print "oops, username is already taken" 
        return False
    except pymongo.errors.OperationFailure: 
        print "oops, mongo error" 
        return False 

    return True

def make_pw_hash(pw, salt=None): 
    if (salt == None): 
        salt = make_salt();

    return sha256(pw + salt).hexdigest()+","+ salt

def make_salt(): 
    salt = ""
    for i in range(5): 
        salt = salt + choice(ascii_letters) 

    return salt

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]

    if h == make_secure_val(val): 
        return val

def start_session(email):
    sessions = db.get_user_sessions_collection()

    session = { 'email': email }

    try:
        sessions.insert(session)

        return str(session['_id'])
    except:
        print "Unexpected error on start session", exc_info()[0]
        return -1

def end_session(session_id):
    sessions = db.get_user_sessions_collection()

    try:
        id = bson.objectid.ObjectId(session_id)

        sessions.remove({'_id': id})
    except:
        print "Unexpected error on end session", exc_info()[0]
    
    return

def get_session(session_id):
    sessions = db.get_user_sessions_collection()

    # this may fail because the string may not be a valid bson objectid
    try:
        id = bson.objectid.ObjectId(session_id)
    except:
        print "Get session: bad session_id", exc_info()[0]
        return None

    session = sessions.find_one({'_id':id})

    return session
