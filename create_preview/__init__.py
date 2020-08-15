from flask import Flask, Response, request
import base64
from create_preview.image_creator.app import ImageCreator, CONFIG_DATA
import json
from marshmallow import Schema, fields, validates, ValidationError

APP = Flask(__name__)

class LinesSchema(Schema):
    line1 = fields.Str(allow_none=True, required=True)
    line2 = fields.Str(allow_none=True, required=True)
    line3 = fields.Str(allow_none=True, required=True)
    line4 = fields.Str(allow_none=True, required=True)

class ImagePreviewInputSchema(Schema):
    font_type = fields.Str(required=True)
    paper_type = fields.Str(required=True)
    paper_color = fields.Str(required=True)
    alignment = fields.Str(required=True)
    text_color = fields.Str(required=True)
    quantity = fields.Int(required=True)
    lines = fields.Nested(LinesSchema, required=True)

    @validates('font_type')
    def valid_font(self, value):
        if value not in CONFIG_DATA["font-types"]:
            raise ValidationError("Font is not supported!")
    
    @validates('alignment')
    def valid_alignment(self, value):
        if value not in CONFIG_DATA["alignments"]:
            raise ValidationError("Alignment not supported")
    
    @validates('text_color')
    #pylint: disable=no-self-argument
    def valid_text_color(self, value):
        if value not in CONFIG_DATA["text-colors"]:
            raise ValidationError("Text-color not supported.")
    
    @validates('quantity')
    #pylint: disable=no-self-argument
    def valid_quantity(self, value):
        if value not in CONFIG_DATA["quantities"]:
            raise ValidationError("Quantity not allowed.")

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