from PIL import Image, ImageDraw, ImageFont, ImageColor
import importlib
import json
import os
import base64
from io import BytesIO

resources_path = os.path.join(os.getcwd(), "create_preview", "resources")

# importing config
with open(os.path.join(resources_path, "config.json")) as config_json:
    data = json.load(config_json)

CONFIG_DATA = data

class ImageCreator(object):
    def __init__(self):
        self.font_type = None
        self.paper_type = None
        self.paper_color = None
        self.alignment = None
        self.text_color = None
        self.quantity = None
        self.lines = None

    # Setting Font
    def set_font_type(self, font_type_string):
        status = {}
        if font_type_string in data["font-types"].keys():
            self.font_type = os.path.join(resources_path, data["font-types"][font_type_string])
            status["error"] = False
        else:
            status["error"] = True
            status["message"] = "Invalid font_type"

        return status

    # Setting Paper Type
    def set_paper_type(self, paper_type_string):
        status = {}
        if paper_type_string in data.keys():
            self.paper_type = paper_type_string
            status["error"] = False
        else:
            status["error"] = True
            status["message"] = "Invalid paper_type"
        return status

    # Setting Paper Color
    def set_paper_color(self, paper_color_string):
        status = {}
        if self.paper_type == None:
            status["error"] = True
            status["message"] = "paper_type must be set before paper_color"
        else:
            if paper_color_string in data[self.paper_type].keys():
                self.paper_color = os.path.join(resources_path, data[self.paper_type][paper_color_string])
                status["error"] = False
            else:
                status["error"] = True
                status["message"] = "Invalid paper_color"
        return status
    
    # Setting Alignment
    def set_alignment(self, alignment_string):
        status = {}
        if alignment_string in data["alignments"]:
            self.alignment = alignment_string
            status["error"] = False
        else:
            status["error"] = True
            status["message"] = "Invalid alignment_string"
        return status
    
    # Setting Text Color
    def set_text_color(self, text_color_string):
        status = {}
        if text_color_string in data["text-colors"].keys():
            self.text_color = data["text-colors"][text_color_string]
            status["error"] = False
        else:
            status["error"] = True
            status["message"] = "Invalid text_color"
        return status
    
    # Setting Quantity
    def set_quantity(self, quantity):
        status = {}
        if int(quantity) in data["quantities"]:
            self.quantity = quantity
            status["error"] = False
        else:
            status["error"] = True
            status["message"] = "Invalid quantity amount"
        return status
    
    # Setting Lines
    def set_lines(self, lines):
        status = {}
        status["error"] = False
        self.lines = lines

        """ if font_type_string in data["font-types"].keys():
            self.font_type = ImageFont.load(os.path.join(resources_path, data["font-types"][font_type_string]))
            status["error"] = False
        else:
            status["error"] = True """
        
        return status
    
    # Setting all values
    def set_all(self, params):
        all_statuses = []
        response = {}

        all_statuses.append(self.set_font_type(params["font_type"]))
        all_statuses.append(self.set_paper_type(params["paper_type"]))
        all_statuses.append(self.set_paper_color(params["paper_color"]))
        all_statuses.append(self.set_alignment(params["alignment"]))
        all_statuses.append(self.set_text_color(params["text_color"]))
        all_statuses.append(self.set_quantity(params["quantity"]))
        all_statuses.append(self.set_lines(params["lines"]))

        all_statuses = [status for status in all_statuses if status["error"]]

        if len(all_statuses) > 0:
            response["error"] = True
            response["statuses"] = all_statuses
        else:
            response["error"] = False

        return response

    # Create image using values
    def generate_image(self):
        image_size = data["paper_size"][self.paper_type]['w'], data["paper_size"][self.paper_type]['h']
        background = Image.open(self.paper_color, 'r')
        background = background.resize(image_size)
        canvas = Image.new('RGB', image_size)
        canvas.paste(background)

        font_size = 16

        # Placing text
        draw = ImageDraw.Draw(canvas)

        font = ImageFont.truetype(self.font_type, font_size)

        if "bottom" in self.alignment:
            text_values = [line for line in self.lines.values() if not line == ""]
            print("BOTTOM:", text_values)
            text_content = ", ".join(text_values)

        else: 
            text_content = "\n".join(self.lines.values())

        if "bernhard" in self.font_type:
            text_content = text_content.upper()

        text_size = draw.multiline_textsize(text_content, font=font)

        while text_size[0] > (image_size[0] - self.mm_to_pixels(5)):
            font_size = font_size - 1
            font = ImageFont.truetype(self.font_type, font_size)
            text_size = draw.multiline_textsize(text_content, font=font)
            
        coords, alignment = self.get_size_information(image_size, text_size, alignment=self.alignment)
        
        draw.multiline_text(coords, text_content, fill=self.text_color, font=font, align=alignment)
        
        # Saving bytes and encoding as base64
        buffered = BytesIO()
        canvas.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str
    
    def mm_to_pixels(self, mm):
        return mm * 3.779527559

    def get_size_information(self, canvas_size, text_size, alignment="right_left"):
        CANVAS_W, CANVAS_H = canvas_size
        TEXT_W, TEXT_H = text_size

        if "right" in alignment:
            if "left" in alignment:
                text_alignment = "left"
            else:
                text_alignment = "right"
            
            x = CANVAS_W - TEXT_W - self.mm_to_pixels(5) 
            y = self.mm_to_pixels(2)
        elif "top" in alignment:
            text_alignment = "center"
            x = (CANVAS_W - TEXT_W)/2
            y = self.mm_to_pixels(4)
        else:
            text_alignment = "center"
            x = (CANVAS_W - TEXT_W)/2
            y = CANVAS_H - TEXT_H - self.mm_to_pixels(4)
        
        return (x, y), text_alignment
        

