import bottle

import cgi
import re
from datetime import datetime
import random
import hmac
import user
import sys
import os
from pymongo import MongoClient

from os.path import dirname

import user
import database as db

appPath = dirname(__file__)

@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=os.path.join(appPath, 'static'))

@bottle.route("/")
def blog_index():
    posts = get_formatted_posts()
    user = login_check()

    return bottle.template('blog_index', { 'posts': posts, 'user': user })

@bottle.route("/post/<permalink>")
def get_post(permalink="notfound"):
    print "About to query on permalink ", permalink

    permalink = cgi.escape(permalink)
    path_re = re.compile(r"^([^\.]+).json$")

    post = get_post_by_permalink(permalink)

    if post == None:
        bottle.redirect("/PostNotFound")
    
    user = login_check()
    comment = { 'author': user, 'email': user, 'message': '' }

    return bottle.template("post_view", { 'post': post, 'user': user, 'comment': comment, 'errors': None })

@bottle.route("/newpost")
def get_newpost():
    if login_check():
        return bottle.template("post_new", dict(subject="", body="",errors="", tags=""))
    return bottle.redirect('/unauthorized')

@bottle.post("/newpost")
def post_newpost():
    user = login_check()
    if user == None:
        return bottle.redirect('/unauthorized')

    title = bottle.request.forms.get("subject")
    post = bottle.request.forms.get("body")
    tags = bottle.request.forms.get("tags")

    # Check mandatory fields
    if (title == "" or post == ""):
        errors = "Posts must contain a tittle and blog entry"
        return bottle.template("post_new", dict(
            subject=cgi.escape(title, quote = True),
            body=cgi.escape(post, quote=True),
            tags=tags,
            errors=errors))
    
    escaped_post = cgi.escape(post, quote = True)

    newline = re.compile('\r?\n')
    formatted_post = newline.sub("<p>",escaped_post)

    tags = extrac_tags(tags)

    permalink = insert_post(title, post, tags, user)

    bottle.redirect("/post/" + permalink)

@bottle.post("/comment")
def post_comment():
    # Get form data
    author = bottle.request.forms.get('name')
    email = bottle.request.forms.get('email')
    message = bottle.request.forms.get('message')
    permalink = bottle.request.forms.get('permalink')

    permalink = cgi.escape(permalink)

    post = get_post_by_permalink(permalink)

    if post == None:
        return bottle.redirect('PostNotFound')

    if author or email or message:
        try:
            print "About to insert new comment..."
            
            comment = { 'author': author, 'email': email, 'message': message, 'date': datetime.utcnow() }
            insert_comment(permalink, comment)

            print "New comment inserted, redirecting to post"
        except Exception as e:
            print "New comment unexpected error", sys.exc_info()[0]
            a = sys.exc_info()

            errors = "Sorry, we couldn't save you comment. Please try again."
            return bottle.template("post_view", dict(post=post, username="indefinido", errors=errors, comment=comment))
    else:
        comment = { 'author': '', 'email': '', 'message': '' }

        errors="Post must contain your name and an actual comment."

        print "New comment error... returning form with errors"
        return bottle.template("post_view", dict(post=post, username="indefinido", errors=errors, comment=comment))
    
    return bottle.redirect("post/" + permalink)

@bottle.route("/PostNotFound")
def get_post_not_found():
    return bottle.template("post_not_found")

@bottle.route("/unauthorized")
def get_unauthorized():
    return bottle.template("unauthorized")

@bottle.route("/tag/<tag>")
def get_posts_by_tag(tag):
    tag = cgi.escape(tag)
    posts = get_formatted_posts(where = {'tags': tag})

    return bottle.template("tag_search", { 'tag': tag, 'posts': posts, 'username': user })

@bottle.get("/signup")
def get_signup():
    if login_check():
        return bottle.redirect("/welcome")
    return bottle.template("user_signup", { 'name': "", 'password': "", 'email': "", 'errors': {}} )

@bottle.post("/signup")
def post_signup():
    name = bottle.request.forms.get("name")
    email = bottle.request.forms.get("email")
    password = bottle.request.forms.get("password")

    errors = { }

    if user.validate_signup(email, password, errors): 
        if user.newuser(email, password):
            session_id = user.start_session(email)
            print session_id 
            cookie = user.make_secure_val(session_id) 
            bottle.response.set_cookie("session", cookie)
            bottle.redirect("/welcome")
        else:            
            errors['email_error'] = "Email already in use. Please choose another" 
    else: 
        print "user did not validate" 

    return bottle.template("user_signup", { 'name': cgi.escape(name), 'password': '', 'email': cgi.escape(email), 'errors': errors} )

@bottle.get("/signin")
def get_signin():
    if login_check():
        return bottle.redirect("/welcome")
    return bottle.template("user_signin", { 'email': '', 'password': '', 'error': '' })

@bottle.post("/signin")
def post_signin():
    email = bottle.request.forms.get("email")
    password = bottle.request.forms.get("password")

    if user.validate_login(email, password):
        session_id = user.start_session(email)

        if session_id == -1:
            bottle.redirect("/error")
        
        cookie = user.make_secure_val(session_id)

        bottle.response.set_cookie("session", cookie)
        bottle.redirect("/welcome")
    else:
        return bottle.template("login", { 'email': cgi.escape(email), 'password':'', 'error': 'Invalid login' })

@bottle.route('/logout')
def logout():
    cookie = bottle.request.get_cookie('session')

    if cookie:
        session_id = user.check_secure_val(cookie)

        if session_id:
            print "Clearing session..."
            user.end_session(session_id)
            print "Session cleared"

            bottle.redirect('/signin')
        else:
            print "Session is not valid"

        bottle.request.set_cookie('session', '')
    else:
        print "No session cookie"
    
    bottle.redirect('/signin')

@bottle.route("/welcome")
def get_welcome():
    if login_check() == None:
        return bottle.redirect("/unauthorized")

    # check for a cookie, if present, then extract value 
    user = login_check()
    if (user): 
        return bottle.template("user_welcome", { 'user': user })
    else:
        print "Welcome can't identify user...redirecting to signup" 
        bottle.redirect("/signup") 

def login_check():
    cookie = bottle.request.get_cookie("session")

    if(cookie):
        session_id = user.check_secure_val(cookie)

        if session_id:
            session = user.get_session(session_id)
            
            if session:
                return session['email']
        else:
            print "No secure session_id"
    else:
        print "No cookie..."
    return None

def extrac_tags(tags):
    whitespace = re.compile('\s')
    nowhite = whitespace.sub("",tags)
    l_tags = nowhite.split(',')

    cleaned = []
    for tag in l_tags:
        if tag not in cleaned and tag != "":
            cleaned.append(tag)

    return cleaned

def insert_post(title, body, tags, author):
    print "Inserting post....", title

    posts = db.get_posts_collection()

    # Combine everything that isn't alphanumeric
    exp = re.compile('\W')
    whitespace = re.compile('\s')
    temp_title = whitespace.sub('_', title)
    permalink = exp.sub('', temp_title)

    post = {
        "title": title,
        "author": author,
        "body": body,
        "permalink": permalink,
        "tags": tags,
        "date": datetime.utcnow()
    }

    try:
        result = posts.insert_one(post)
        print "Post inserted!", result.inserted_id

    except:
        print "Error inserting post", sys.exc_info()[0]
    
    return permalink

def insert_comment(post_permalink, comment):
    posts = db.get_posts_collection()

    posts.update({ 'permalink': post_permalink }, {'$push': { 'comments': comment } }, upsert=False)

def get_formatted_posts(where=None, limit=10):
    print "Getting posts"

    posts = db.get_posts_collection()

    cursor = posts.find(where).sort('date', direction=-1).limit(limit)

    formatted_posts = []

    for post in cursor:
        print "Reading post", post['title']

        if 'tags' not in post:
            post['tags'] = []

        if 'comments' not in post:
            post['comments'] = []
        
        formatted_posts.append({
            'title': post['title'],
            'body': post['body'],
            'date': post['date'].strftime("%A, %B %d %Y at %I:%M%p"),
            'permalink': post['permalink'],
            'author': post['author'],
            'tags': post['tags'],
            'comments': post['comments']
        })

    return formatted_posts

def get_post_by_permalink(permalink):
    posts = db.get_posts_collection()

    post = posts.find_one({'permalink': permalink})
    
    if post == None:
        return post

    post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p")

    if 'tags' not in post:
        post['tags'] = []

    if 'comments' not in post:
        post['comments'] = []
    else:
        for comment in post['comments']:
            comment['date'] = comment['date'].strftime("%A, %B %d %Y at %I:%M%p")
    
    return post

bottle.TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))
bottle.debug(True)
bottle.run(host='localhost',port=8082)
