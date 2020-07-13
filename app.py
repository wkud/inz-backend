from flask import Flask, request
from flask_restful import Resource, Api

app = Flask("inz")
api = Api(app)

collection = []
array = {}


class Endpoint(Resource):
    def get(self):
        return {"about": "Hello World!"}

    def post(self):
        args = request.args
        index = int(args['index'])
        value = int(args['value'])
        array[index] = value
        return array


class UrlEndpoint(Resource):
    def post(self, name):
        if request.method == 'POST':
            data = request.get_json()
        collection.append({name: data})
        return collection


api.add_resource(Endpoint, "/")
api.add_resource(UrlEndpoint, "/<string:name>")


if __name__ == "__main__":
    app.run(debug=True)
