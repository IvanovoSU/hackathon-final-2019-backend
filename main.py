import os
import sys
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('main.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS deprecated
db = SQLAlchemy(app)

def print_err(s):
    print(s, file=sys.stderr)

def generate_page(data):
    with open('include/header.html', 'r') as header:
        page=header.read()
    page += data
    with open('include/footer.html', 'r') as footer:
        page+=footer.read()
    return page

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('include/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('include/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('include/fonts', path)

@app.route('/', methods = ["GET", "POST"])
def root():
    if request.method == 'POST':

        db.session.commit() 
    return "Ok"

app.run()
