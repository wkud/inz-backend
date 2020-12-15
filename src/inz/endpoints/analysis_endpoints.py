from flask import request
from flask_restful import Resource
from flask_api import status
from flask_jwt import jwt_required, current_identity
from inz import api
from inz.services.category_service import CategoryService


class CategoryAnalysisEndpoint(Resource):
    # http://127.0.0.1:5000/category/analysis
    decorators = [jwt_required()]

    def post(self):
        data = request.get_json()
        print(data)
        try:
            analysis = CategoryService.get_category_analysis(
                data.get('period_start'),
                data.get('period_end'),
                current_identity.categories,
                current_identity.expenses)
            return {'analysis': analysis}
        except ValueError:
            return 'Invalid date strings', status.HTTP_400_BAD_REQUEST
        except AttributeError:
            return 'Invalid request body', status.HTTP_400_BAD_REQUEST


api.add_resource(CategoryAnalysisEndpoint, '/analysis')
