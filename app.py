from flask import Flask, Response, request
import requests
import json
from flask_cors import CORS

from utils import make_url, perform_search

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})


@app.route("/")
def test():
    return "Ok."


@app.route("/search/all")
def search():
    start_from = request.args.get('start_from');
    data = perform_search(start_from)

    resp = Response(data)
    resp.headers['content-type'] = 'application/json'
    return resp







