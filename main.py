import os
import sys
from sqlalchemy import Column, Integer, String  
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('main.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS deprecated
app.config['SECRET_KEY'] = '.}kp4Gj7egnX-~,;ABEU'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def init_db():
    db.create_all()

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(120), unique=True)

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True

    def get_id(self):
        return self.id

def print_err(s):
    print(s, file=sys.stderr)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('include/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('include/css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('include/fonts', path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next = request.args.get('next')
        if next == 'logout':
            next = ''
        user = User.query.filter_by(username=username, password=password).first()
        if not (user is None):  
            login_user(user, remember=True)
            return redirect(next or flask.url_for('/admin'))
        else:
            return redirect(url_for('login', next=next))
    else:
        with open('include/login.html', 'r') as page:
            data=page.read()
        return data
    
@app.route('/admin', methods = ["GET", "POST"])
@login_required
def admin():
    with open('include/admin.html', 'r') as page:
        data=page.read()
    return data

@app.route('/', methods = ["GET", "POST"])
def root():
    with open('include/index.html', 'r') as page:
        data=page.read()
    return data

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin'))

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user
    return None

