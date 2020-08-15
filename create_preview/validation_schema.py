from marshmallow import Schema, fields, validates, ValidationError
from create_preview.image_creator.app import CONFIG_DATA

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
