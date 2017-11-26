"""Hello Word"""
import bottle

@bottle.route('/')
def home_page():
    """Gets the home page"""
    return bottle.template('hello_world.tpl', username="Caio")

@bottle.route('/test')
def test_page():
    """test_page() -> string"""
    return "this is a test page"

@bottle.route('/fruits')
def fruit_form():
    """Return the fruits form"""
    fruits = ['apple', 'orange', 'banana', 'peach']
    return bottle.template('fruit_form', {fruits: fruits})

@bottle.post('/fruits/favorite')
def favorite_fruit():
    """Sets a fruit as favorite"""
    fruit = bottle.request.forms.get("fruit")
    if fruit is None or fruit == "":
        fruit = "No fruid selected"

    return bottle.template('selected_fruit.tpl', {fruit: fruit})

bottle.debug(True)
bottle.run(host='localhost', port=8080)
