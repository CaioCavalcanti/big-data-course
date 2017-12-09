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


@bottle.route("/")
def blog_index():
    posts = get_formatted_posts()

    return bottle.template('blog_index', dict(posts=posts))

@bottle.route("/post/<permalink>")
def get_post(permalink="notfound"):
    db = connect_db()
    posts = db.posts

    permalink = cgi.escape(permalink)
    path_re = re.compile(r"^([^\.]+).json$")

    print "About to query on permalin ", permalink

    post = posts.find_one({'permalink': permalink})

    if post == None:
        bottle.redirect("PostNotFound")
    
    post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p")

    if 'tags' not in post:
        post['tags'] = []

    if 'comments' not in post:
        post['comments'] = []
    
    comment = {
        'name': '',
        'email': '',
        'message': ''
    }

    return bottle.template("post_view", dict(post=post, username="undefined", comment=comment))

@bottle.route("/newpost")
def get_newpost():
    return bottle.template("post_new", dict(subject="", body="",errors="", tags=""))

@bottle.post("/newpost")
def post_newpost():
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

    permalink = insert_post(title, post, tags, "undefined")

    bottle.redirect("/post/" + permalink)

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

    # DB
    db = connect_db()
    posts = db.posts

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

def get_formatted_posts():
    print "Getting posts"

    db = connect_db()
    posts = db.posts
    cursor = posts.find().sort('date', direction=-1).limit(10)

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

def connect_db():
    connection = MongoClient('localhost', 27017)
    db = connection.blog
    return db

bottle.TEMPLATE_PATH.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "views")))
bottle.debug(True)
bottle.run(host='localhost',port=8082)
