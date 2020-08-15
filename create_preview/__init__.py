from flask import Flask, Response, request
import base64
from create_preview.image_creator.app import ImageCreator, CONFIG_DATA
import json
from create_preview.validation_schema import ImagePreviewInputSchema

APP = Flask(__name__)

@APP.route('/')
def home():
    return Response("Hello")

@APP.route('/generate-image', methods=['POST'])
def generate_image():
    values = request.json
    input_schema = ImagePreviewInputSchema()
    request_errors = input_schema.validate(request.json)
    
    if request_errors:
        return Response(json.dumps(request_errors), mimetype="application/json", status=400)

    preview = ImageCreator()
    factory_errors = preview.set_all(request.json)

    if factory_errors["error"]:
        return Response(json.dumps(factory_errors["statuses"]), mimetype="application/json", status=400)


    values = request.json
    print(values)

    return Response(status=200)

def create_app():
    return APP