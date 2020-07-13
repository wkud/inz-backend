from flask import Flask, request
from flask_restful import Resource, Api

app = Flask("inz")
api = Api(app)

collection = []
array = {}


class Endpoint(Resource):
    # http://127.0.0.1:5000/
    def get(self):
        return {"about": "Hello World!"}
        # response: {"about": "Hello World!"}

    # http://127.0.0.1:5000?index=4&value=10
    def post(self):
        args = request.args
        index = int(args['index'])
        value = int(args['value'])
        array[index] = value
        return array
        # response: { "4": 10 }


class UrlEndpoint(Resource):
    # http://127.0.0.1:5000/some_name
    def post(self, name):
        if request.method == 'POST':
            data = request.get_json()
        collection.append({name: data})
        return collection
        # response: { "some_name": 10 }


api.add_resource(Endpoint, "/")
api.add_resource(UrlEndpoint, "/<string:name>")


if __name__ == "__main__":
    app.run(debug=True)
