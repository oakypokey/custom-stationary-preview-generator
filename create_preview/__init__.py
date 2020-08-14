from flask import Flask, Response

APP = Flask(__name__)

@APP.route('/')
def home():
    return Response("Hello")

def create_app():
    return APP