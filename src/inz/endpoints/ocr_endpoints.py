from flask_restful import Resource
from inz import api
from inz.services.ocr_service import OcrUtility


class OcrEndpoint(Resource):
    # http://127.0.0.1:5000/ocr/{img_name}

    def get(self, img_name):
        text = OcrUtility.recognize(img_name)
        return {'result': text}


api.add_resource(OcrEndpoint, '/ocr/<img_name>')
