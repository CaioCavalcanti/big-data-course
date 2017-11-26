import logging

from flask import request
from flask_restplus import Resource
from pf.api.business import get_all_categories, create_category
from pf.api.serializer import category
from pf.api.restplus import api

log = logging.getLogger(__name__)

ns = api.namespace('categories', description='Operations related to categories')

@ns.route('/')
class CategoryCollection(Resource):
    @api.marshal_list_with(category)
    def get(self):
        """
        Returns list of categories.
        """
        return list(get_all_categories())

    @api.response(201, 'Category successfully created.')
    @api.expect(category)
    def post(self):
        """
        Creates a new category.
        """
        data = request.json
        result = create_category(data)
        return result, 201