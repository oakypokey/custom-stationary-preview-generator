from flask import Flask, Response, request
from create_preview.image_creator.app import ImageCreator
import json
from create_preview.validation_schema import ImagePreviewInputSchema
import uuid

APP = Flask(__name__, static_url_path='', static_folder='resources', template_folder='shopify_api/templates')

import create_preview.shopify_api.shopify_routes

@APP.route('/')
def home():
    return Response("Hello")

@APP.route('/generate-image', methods=['GET'])
def generate_image():
    # First set of validation
    input_schema = ImagePreviewInputSchema()
    json_payload = json.loads(request.args.get('json'))
    request_errors = input_schema.validate(json_payload)
    
    if request_errors:
        return Response(json.dumps(request_errors), mimetype="application/json", status=400)

    # Create new ImageCreator
    preview = ImageCreator()
    factory_errors = preview.set_all(json_payload)

    # Throw any errors from ImageCreator
    if factory_errors["error"]:
        return Response(json.dumps(factory_errors["statuses"]), mimetype="application/json", status=400)

    preview_image = preview.generate_image().decode('utf-8')

    payload = 'data:image/png;base64, {preview_image}'.format(preview_image=preview_image)

    return Response(payload, status=200)

@APP.route('/static/product_handlers.js')
def product_handler():
    return APP.send_static_file("product_handlers.js")

def create_app():
    return APP