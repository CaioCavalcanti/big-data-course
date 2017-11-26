# Personal Finances API
This project is an example of a RESTful API using Flask, MongoDB, Swagger UI and Flask-RESTPlus.

This projects is based on [postrational/rest_api_demo](https://github.com/postrational/rest_api_demo)


## Running the project
1. Clone this repo
```
cd /path/to/your/workspace/
git clone https://github.com/CaioCavalcanti/big-data-course.git
cd big-data-course/MongoDB/Exercises/personal_finances
```

2. Create a virtual environment, activate it and install the dependencies
```
python -m virtualenv venv
call venv\Scripts\activate
pip install -r requirements.txt
```

3. Make sure the current working directory is on your PYTHONPATH and start the app
```
set PYTHONPATH =.
python pf/app.py
```

4. Now evetything should be ready! Access [http://localhost:8888/api/](http://localhost:8888/api/) to check the API documentation

## References
- [Building beautiful REST APIs using Flask, Swagger UI and Flask-RESTPlus](http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/)