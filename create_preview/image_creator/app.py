from PIL import Image, ImageDraw, ImageFont
import importlib
import json
import os

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
            self.font_type = ImageFont.truetype(os.path.join(resources_path, data["font-types"][font_type_string]))
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
        print("This is where the image is generated")        
        

