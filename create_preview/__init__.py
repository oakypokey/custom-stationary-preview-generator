from flask import Flask, Response, request
from create_preview.image_creator.app import ImageCreator
import json
from create_preview.validation_schema import ImagePreviewInputSchema

APP = Flask(__name__)

@APP.route('/')
def home():
    return Response("Hello")

@APP.route('/generate-image', methods=['POST'])
def generate_image():
    # First set of validation
    input_schema = ImagePreviewInputSchema()
    request_errors = input_schema.validate(request.json)
    
    if request_errors:
        return Response(json.dumps(request_errors), mimetype="application/json", status=400)

    # Create new ImageCreator
    preview = ImageCreator()
    factory_errors = preview.set_all(request.json)

    # Throw any errors from ImageCreator
    if factory_errors["error"]:
        return Response(json.dumps(factory_errors["statuses"]), mimetype="application/json", status=400)

    preview_image = preview.generate_image().decode('utf-8')

    payload = '<img src="data:image/png;base64, {preview_image}" alt="Preview Image" />'.format(preview_image=preview_image)

    return Response(payload, status=200)

def create_app():
    return APP