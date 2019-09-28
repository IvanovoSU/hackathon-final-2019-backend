# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, Integer, String  
from flask import Flask, request, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, UserMixin, LoginManager, login_required, login_user, logout_user
from xlrd import * 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('main.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS deprecated
app.config['SECRET_KEY'] = '.}kp4Gj7egnX-~,;ABEU'
db = SQLAlchemy(app)

region_name_to_id = {
    'Белгородская область': 36,
    'Владимирская область': 37,
    'Ивановская область': 41,
}

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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

class Map(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(Integer, db.ForeignKey('user.id'))
    city = Column(String(120), unique=True)
    edit_link = Column(String(10000))
    show_link = Column(String(10000))

    def __init__(self, author, city, edit_link, show_link):
        self.author = author
        self.city = city
        self.edit_link = edit_link
        self.show_link = show_link

class Region(db.Model):
    id = Column(Integer, primary_key=True)
    postgraduate = Column(Integer)
    higher = Column(Integer)
    higherip = Column(Integer)
    middle = Column(Integer)
    basic = Column(Integer)
    noeducation = Column(Integer)
    nothing = Column(Integer)

    def __init__(self, id, postgraduate, higher, higherip, middle, basic, noeducation, nothing):
        self.id = id
        self.postgraduate = postgraduate
        self.higher = higher
        self.higherip = higherip
        self.middle = middle
        self.basic = basic
        self.noeducation = noeducation
        self.nothing = nothing

class RegionDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    regionid = Column(Integer, db.ForeignKey('region.id'))
    datatype = Column(Integer)
    gender = Column(Integer)
    total = Column(Integer)
    y1517 = Column(Integer)
    y1819 = Column(Integer)
    y2024 = Column(Integer)
    y2529 = Column(Integer)
    y3034 = Column(Integer)
    y3539 = Column(Integer)
    y4044 = Column(Integer)
    y4549 = Column(Integer)
    y5054 = Column(Integer)
    y5559 = Column(Integer)
    y6064 = Column(Integer)
    y6569 = Column(Integer)
    y70p =  Column(Integer)
    workable = Column(Integer)
    bworkable = Column(Integer)
    y1629 = Column(Integer)

    def __init__(self, regionid, datatype, gender, data):
        self.regionid = regionid
        self.datatype = datatype
        self.gender = gender
        self.total = data[0]
        self.y1517 = data[1]
        self.y1819 = data[2]
        self.y2024 = data[3]
        self.y2529 = data[4]
        self.y3034 = data[5]
        self.y3539 = data[6]
        self.y4044 = data[7]
        self.y4549 = data[8]
        self.y5054 = data[9]
        self.y5559 = data[10]
        self.y6064 = data[11]
        self.y6569 = data[12]
        self.y70p =  data[13]
        self.workable = data[14]
        self.bworkable = data[15]
        self.y1629 = data[16]

def print_err(s):
    print(s, file=sys.stderr)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('fonts', path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        next = request.args.get('next')
        if next and ('logout' in next):
            next = None
        user = User.query.filter_by(username=username, password=password).first()
        if not (user is None):  
            login_user(user, remember=False)
            return redirect(next or url_for('admin'))
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

def get_maps():
    return Map.query.all()

@app.route('/admin/editmaps', methods = ["GET", "POST"])
@login_required
def editmaps():
    if request.method == 'POST':
        city = request.form['city']
        edit_link = request.form['edit_link']
        show_link = request.form['show_link']
        nmap = Map(current_user.id, city, edit_link, show_link)
        db.session.add(nmap)
        db.session.commit()

    with open('include/editmaps.html', 'r') as page:
        data=page.read()
    mps = get_maps()
    mps_str = ""
    for i in range(len(mps)):
        user = User.query.filter_by(id = mps[i].author).first()
        mps_str += "<tr>\n"
        mps_str += "<td>" + mps[i].city + "</td>\n"
        mps_str += "<td>" + user.username + "</td>\n"
        if user.id == current_user.id:
            mps_str += "<td><a href=" + mps[i].edit_link + ">Изменить</a></td>\n"
        else:
            mps_str += "<td>Изменять можно только города, добавленные вами</td>\n"    
        mps_str += "</tr>\n"
    data = data.replace('%MAP_TABLE%', mps_str)
    return data

@app.route('/maps', methods = ["GET", "POST"])
def maps():
    ct = 1
    if 'city_id' in request.form:
        ct = int(request.form['city_id'])
    with open('include/maps.html', 'r') as page:
        data=page.read()
    mps = get_maps()
    mps_str = ''
    for i in range(len(mps)):
        mps_str += '<option value="' + str(mps[i].id) + '">'+ mps[i].city + "</option>\n"  
    data = data.replace('%MAPS%', mps_str)
    data = data.replace('%MAP%', mps[ct-1].show_link)
    data = data.replace('%MAP_NUM%', str(ct))
    return data

def calcdata(datatype, filename):
    wb = open_workbook(filename)


@app.route('/admin/adddata', methods = ["GET", "POST"])
@login_required
def adddata():
    if request.method == 'POST':
        datatype = int(request.form['datatype'])
        if len(request.files) > 0:
            file = request.files['file']
            if file:
                filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/'+ str(datatype) +'.xls')
                file.save(filename)
                calcdata(datatype, filename)

    with open('include/adddata.html', 'r') as page:
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

