from flask_restplus import fields
from pf.api.restplus import api

category = api.model('Categories', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a category'),
    'name': fields.String(required=True, description='Category name')
})
