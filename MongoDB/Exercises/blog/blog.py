import bottle
import cgi
import re
import random
import hmac
import user
import sys
import os
from datetime import datetime
from pymongo import MongoClient
from os.path import dirname, join, abspath

# Local
import database as db
import user
import category


@bottle.route("/")
def blog_index():
    posts = get_formatted_posts()
    user = get_current_user()

    return bottle.template('blog_index', {'posts': posts, 'user': user})


@bottle.route("/post/<permalink>")
def get_post(permalink="notfound"):
    print "About to query on permalink ", permalink

    permalink = cgi.escape(permalink)
    path_re = re.compile(r"^([^\.]+).json$")

    post = get_post_by_permalink(permalink)

    if post is None:
        bottle.redirect("/post/" + permalink + "/not_found")

    user = get_current_user()
    comment = {'author': user, 'email': user, 'message': ''}

    return bottle.template("post_view", {'post': post, 'user': user, 'comment': comment, 'errors': None})


@bottle.route("/post/new")
def get_newpost():
    if get_current_user():
        categories = category.get_category_options()

        return bottle.template("post_new", {'title': "", 'body': "",  'tags': "", 'category': "", 'categories': categories, 'errors': ""})
    return bottle.redirect('/unauthorized')


@bottle.post("/post/new")
def post_newpost():
    user = get_current_user()
    if user is None:
        return bottle.redirect('/unauthorized')

    title = bottle.request.forms.get("title")
    body = bottle.request.forms.get("body")
    tags = bottle.request.forms.get("tags")
    category_id = bottle.request.forms.get("category")

    # Check mandatory fields
    if (title == "" or body == ""):
        errors = "Posts must contain a tittle and blog entry"
        return bottle.template("post_new", dict(
            subject=cgi.escape(title, quote=True),
            body=cgi.escape(body, quote=True),
            tags=tags,
            errors=errors))

    escaped_post = cgi.escape(body, quote=True)

    newline = re.compile('\r?\n')
    formatted_post = newline.sub("<p>", escaped_post)

    tags = extrac_tags(tags)

    permalink = insert_post(title, body, category_id, tags, user)

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

    if post is None:
        return bottle.redirect('PostNotFound')

    if author or email or message:
        try:
            print "About to insert new comment..."

            comment = {'author': author, 'email': email,
                       'message': message, 'date': datetime.utcnow()}
            insert_comment(permalink, comment)

            print "New comment inserted, redirecting to post"
        except Exception as e:
            print "New comment unexpected error", sys.exc_info()[0]
            a = sys.exc_info()

            errors = "Sorry, we couldn't save you comment. Please try again."
            return bottle.template("post_view", dict(post=post, username="indefinido", errors=errors, comment=comment))
    else:
        comment = {'author': '', 'email': '', 'message': ''}

        errors = "Post must contain your name and an actual comment."

        print "New comment error... returning form with errors"
        return bottle.template("post_view", dict(post=post, username="indefinido", errors=errors, comment=comment))

    return bottle.redirect("post/" + permalink)


@bottle.route("/post/<permalink>/not_found")
def get_post_not_found(permalink):
    return bottle.template("post_not_found", { 'post': permalink})


@bottle.route("/unauthorized")
def get_unauthorized():
    return bottle.template("unauthorized")


@bottle.route("/tag/<tag>")
def get_posts_by_tag(tag):
    tag = cgi.escape(tag)
    posts = get_formatted_posts(where={'tags': tag})

    return bottle.template("tag_search", {'tag': tag, 'posts': posts, 'username': user})


@bottle.get("/signup")
def get_signup():
    if get_current_user():
        return bottle.redirect("/welcome")
    return bottle.template("user_signup", {'name': "", 'password': "", 'email': "", 'errors': {}})


@bottle.post("/signup")
def post_signup():
    name = bottle.request.forms.get("name")
    email = bottle.request.forms.get("email")
    password = bottle.request.forms.get("password")

    errors = {}

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

    return bottle.template("user_signup", {'name': cgi.escape(name), 'password': '', 'email': cgi.escape(email), 'errors': errors})


@bottle.get("/signin")
def get_signin():
    if get_current_user():
        return bottle.redirect("/welcome")
    return bottle.template("user_signin", {'email': '', 'password': '', 'error': ''})


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
        return bottle.template("login", {'email': cgi.escape(email), 'password': '', 'error': 'Invalid login'})


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
    user = get_current_user()

    if user:
        return bottle.template("user_welcome", {'user': user})
    return bottle.redirect("/unauthorized")


@bottle.route("/category")
def get_categories():
    if get_current_user() is None:
        return bottle.redirect("/unauthorized")

    categories = category.get_categories(include_info=True)

    return bottle.template("category_list", {'categories': categories})


@bottle.route("/category/new")
def get_new_category():
    if get_current_user() is None:
        return bottle.redirect("/unauthorized")

    return bottle.template("category_new", {'name': '', 'errors': ''})


@bottle.post("/category/new")
def post_new_category():
    current_user = get_current_user()

    if current_user is None:
        return bottle.redirect("/unauthorized")

    name = bottle.request.forms.get("name")

    if name:
        category_created = category.insert_category(
            cgi.escape(name), current_user)

        if category_created:
            return bottle.redirect("/category")
        else:
            errors = "We couldn't create the category, please try again."
    else:
        errors = "Please inform all required fields"

    return bottle.template("category_new", {'name': name, 'errors': errors})


@bottle.route("/category/<category_id>")
def get_posts_by_category(category_id):
    category_id = cgi.escape(category_id)

    cat = category.get_category_by_id(category_id)

    if cat is None:
        return bottle.redirect("/category/" + category_id + "/not_found")

    posts = get_formatted_posts(where={'category_id': category_id})

    return bottle.template("category_search", {'category': cat, 'posts': posts})


@bottle.route("/category/<category_id>/not_found")
def get_category_not_found(category_id):
    return bottle.template("category_not_found", {'category': category_id})


def get_current_user():
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
    nowhite = whitespace.sub("", tags)
    l_tags = nowhite.split(',')

    cleaned = []
    for tag in l_tags:
        if tag not in cleaned and tag != "":
            cleaned.append(tag)

    return cleaned


def insert_post(title, body, category_id, tags, author):
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
        "category_id": category_id,
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

    posts.update({'permalink': post_permalink}, {
                 '$push': {'comments': comment}}, upsert=False)


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

        post['category'] = ''

        if 'category_id' in post:
            post_category = category.get_category_by_id(post['category_id'])

            if post_category:
                post['category'] = post_category['name']

        formatted_posts.append({
            'title': post['title'],
            'body': post['body'],
            'date': post['date'].strftime("%A, %B %d %Y at %I:%M%p"),
            'permalink': post['permalink'],
            'author': post['author'],
            'tags': post['tags'],
            'comments': post['comments'],
            'category': post['category'],
            'category_id': post['category_id']
        })

    return formatted_posts


def get_post_by_permalink(permalink):
    posts = db.get_posts_collection()

    post = posts.find_one({'permalink': permalink})

    if post is None:
        return post

    post['date'] = post['date'].strftime("%A, %B %d %Y at %I:%M%p")

    post['category'] = ''

    if 'category_id' in post:
        post_category = category.get_category_by_id(post['category_id'])

        if post_category:
            post['category'] = post_category['name']

    if 'tags' not in post:
        post['tags'] = []

    if 'comments' not in post:
        post['comments'] = []
    else:
        for comment in post['comments']:
            comment['date'] = comment['date'].strftime(
                "%A, %B %d %Y at %I:%M%p")

    return post


appPath = dirname(__file__)


@bottle.route('/static/css/<filepath:path>')
def server_static(filepath):
    """Tells bottle where to find css files"""
    return bottle.static_file(filepath, root=join(appPath, 'static/css'))


bottle.BaseTemplate.defaults['current_user'] = get_current_user

# Avoiding issues with views folder
bottle.TEMPLATE_PATH.insert(0, abspath(join(appPath, "views")))

bottle.debug(True)
bottle.run(host='localhost', port=8082)
