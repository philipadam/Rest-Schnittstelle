import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)