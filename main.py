# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, Integer, String  
from flask import Flask, request, redirect, url_for, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, UserMixin, LoginManager, login_required, login_user, logout_user
from xlrd import * 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('main.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # SQLALCHEMY_TRACK_MODIFICATIONS deprecated
app.config['SECRET_KEY'] = '.}kp4Gj7egnX-~,;ABEU'
db = SQLAlchemy(app)

region_name_to_id = {
    'Республика Адыгея': 1,
    'Республика Алтай': 2,
    'Республика Башкортостан': 3,
    'Республика Бурятия': 4,
    'Республика Дагестан': 5,
    'Республика Ингушетия': 6,
    'Кабардино-Балкарская Республика': 7,
    'Республика Калмыкия': 8,
    'Карачаево-Черкесская Республика': 9,
    'Республика Карелия': 10,
    'Республика Коми': 11,
    'Республика Крым': 12,
    'Республика Марий Эл': 13,
    'Республика Мордовия': 14,
    'Республика Саха (Якутия)': 15,
    'Республика Северная Осетия': 16,
    'Республика Северная Осетия-Алания': 16,
    'Республика Татарстан': 17,
    'Республика Тыва': 18,
    'Удмуртская Республика': 19,
    'Республика Хакасия': 20,
    'Чеченская Республика': 21,
    'Чувашская Республика': 22,
    'Алтайский край': 23,
    'Забайкальский край': 24,
    'Камчатский край': 25,
    'Краснодарский край': 26,
    'Красноярский край': 27,
    'Пермский край': 28,
    'Приморский край': 29,
    'Ставропольский край': 30,
    'Хабаровский край': 31,
    'Амурская область': 32,
    'Архангельская область': 33,
    'Астраханская область': 34,
    'Белгородская область': 35,
    'Брянская область': 36,
    'Владимирская область': 37,
    'Волгоградская область': 38,
    'Вологодская область': 39,
    'Воронежская область': 40,
    'Ивановская область': 41,
    'Иркутская область': 42,
    'Калининградская область': 43,
    'Калужская область': 44,
    'Кемеровская область': 45,
    'Кировская область': 46,
    'Костромская область': 47,
    'Курганская область': 48,
    'Курская область': 49,
    'Ленинградская область': 50,
    'Липецкая область': 51,
    'Магаданская область': 52,
    'Московская область': 53,
    'Мурманская область': 54,
    'Нижегородская область': 55,
    'Новгородская область': 56,
    'Новосибирская область': 57,
    'Омская область': 58,
    'Оренбургская область': 59,
    'Орловская область': 60,
    'Пензенская область': 61,
    'Псковская область': 62,
    'Ростовская область': 63, 
    'Рязанская область': 64,
    'Самарская область': 65,
    'Саратовская область': 66,
    'Сахалинская область': 67,
    'Свердловская область': 68,
    'Смоленская область': 69,
    'Тамбовская область': 70,
    'Тверская область': 71,
    'Томская область': 72,
    'Тульская область': 73,
    'Тюменская область': 74,
    'Ульяновская область': 75,
    'Челябинская область': 76,
    'Ярославская область': 77,
    'г. Москва': 78,
    'г.Москва': 78,
    'Москва': 78,
    'Санкт-Петербург': 79,
    'г. Санкт-Петербург': 79,
    'г.Санкт-Петербург': 79,
    'Севастополь': 80,
    'Еврейская автономная область': 81,
    'Еврейская авт. область': 81,
    'Ненецкий автономный округ': 82,
    'Ненецкий авт. округ': 82,
    'Ханты-Мансийский автономный округ - Югра': 83,
    'Ханты-Мансийский авт. округ - Югра': 83,
    'Чукотский автономный округ': 84,
    'Чукотский авт. округ': 84,
    'Ямало-Ненецкий автономный округ': 85,
    'Ямало-Ненецкий авт. округ': 85
}

education_to_col = {
    1: 4, #'послевузовское': 4,
    2: 5, #'высшее': 5,
    3: 9, #'неполное высшее': 9,
    4: 10, #'среднеe проф': 10,
    5: 11, #'начальное проф': 11,
    6: 12, #среднее полное
    7: 13, #cреднее основное
    8: 14,#начальное
    9: 15 #'не имеющие начального общего об-разования': 15
}

eduid_to_name = {
    1: 'послевузовское',
    2: 'высшее',
    3: 'неоконченное высшее',
    4: 'среднеe специальное',
    5: 'начальное специальное',
    6: 'среднее общее',
    7: 'основное общее',
    8: 'начальное',
    9: 'без образования'
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

class EducationRegion(db.Model):
    id = Column(Integer, primary_key=True)
    postgraduate = Column(Integer)
    higher = Column(Integer)
    higherip = Column(Integer)
    middleprof = Column(Integer)
    basicprof = Column(Integer)
    middlefull = Column(Integer)
    middlemain = Column(Integer)
    basic = Column(Integer)
    noeducation = Column(Integer)

    def __init__(self, id, postgraduate, higher, higherip, 
                 middleprof, basicprof, middlefull, middlemain, 
                 basic, noeducation):
        self.id = id
        self.postgraduate = postgraduate
        self.higher = higher
        self.higherip = higherip
        self.middleprof = middleprof
        self.basicprof = basicprof
        self.middlefull = middlefull
        self.middlemain = middlemain
        self.basic = basic
        self.noeducation = noeducation

class EducationDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    regionid = Column(Integer, db.ForeignKey('education_region.id'))
    datasubtype = Column(Integer)
    gender = Column(Integer)
    livetype = Column(Integer)
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

    def __init__(self, regionid, gender, livetype, datasubtype, data):
        self.regionid = regionid
        self.datasubtype = datasubtype
        self.gender = gender
        self.livetype = livetype
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

class DemograghyRegion(db.Model):
    id = Column(Integer, primary_key=True)
    born = Column(Integer)
    dead = Column(Integer)

    def __init__(self, id, born, dead):
        self.id = id
        self.born = born
        self.dead = dead

def print_err(s):
    print(s, file=sys.stderr)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

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
        with open('include/login.html', 'r', encoding="utf-8") as page:
            data=page.read()
        return data
    
@app.route('/admin', methods = ["GET", "POST"])
@login_required
def admin():
    with open('include/admin.html', 'r', encoding="utf-8") as page:
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

    with open('include/editmaps.html', 'r', encoding="utf-8") as page:
        data=page.read()
    mps = get_maps()
    mps_str = ""
    for i in range(len(mps)):
        user = User.query.filter_by(id = mps[i].author).first()
        mps_str += "<tr>\n"
        mps_str += "<td>" + mps[i].city + "</td>\n"
        mps_str += "<td>" + user.username + "</td>\n"
        if user.id == current_user.id:
            mps_str += "<td><a class=\"table-link\" href=" + mps[i].edit_link + ">Изменить</a></td>\n"
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
    with open('include/maps.html', 'r', encoding="utf-8") as page:
        data=page.read()
    mps = get_maps()
    mps_str = ''
    for i in range(len(mps)):
        mps_str += '<li><a href="#" onclick="changecity(' + str(mps[i].id) + ')">' + mps[i].city + "</a></li>\n"  
    data = data.replace('%MAPS%', mps_str)
    if len(mps) > 0:
        data = data.replace('%MAP%', mps[ct-1].show_link)
    else:
        data = data.replace('%MAP%', '')
    data = data.replace('%MAP_NUM%', str(ct))
    return data

def calcedudata(datatype, filename):

    def get_subdata(sheet, i, col):
        l = []
        l.append(sheet.cell(i, col).value)
        if col >= 10:
            l.append(sheet.cell(i + 2, col).value)
        else:
            l.append(0)
        if col >= 9:
            l.append(sheet.cell(i + 3, col).value)
        else:
            l.append(0)
        for j in range(11):
            l.append(sheet.cell(i + j + 4, col).value)
        return l


    wb = open_workbook(filename)
    sheet = wb.sheets()[0]
    for i in range(sheet.nrows):
        if sheet.cell(i,1).value in region_name_to_id:
            regid = region_name_to_id[sheet.cell(i,1).value]
            postgraduate = sheet.cell(i+2,4).value
            higher  =  sheet.cell(i+2,5).value
            higherip = sheet.cell(i+2,9).value
            middleprof = sheet.cell(i+2,10).value
            basicprof = sheet.cell(i+2,11).value
            middlefull = sheet.cell(i+2,12).value
            middlemain = sheet.cell(i+2,13).value
            basic = sheet.cell(i+2,14).value
            noeducation = sheet.cell(i+2,15).value
            region = EducationRegion(regid, postgraduate, higher, 
                higherip, middleprof, basicprof, middlefull, middlemain, 
                basic, noeducation) 
            db.session.add(region)

            gender = 1
            livetype = 0
            for ed in range(1, len(education_to_col) + 1):
                datasubtype = ed
                data = get_subdata(sheet, i + 21, education_to_col[ed])
                edd = EducationDetail(regid, gender, livetype, datasubtype, data)
                db.session.add(edd)
            gender = 2
            livetype = 0
            for ed in range(1, len(education_to_col) + 1):
                datasubtype = ed
                data = get_subdata(sheet, i + 40, education_to_col[ed])
                edd = EducationDetail(regid, gender, livetype, datasubtype, data)
                db.session.add(edd)
            gender = 0
            livetype = 1
            for ed in range(1, len(education_to_col) + 1):
                datasubtype = ed
                data = get_subdata(sheet, i + 60, education_to_col[ed])
                edd = EducationDetail(regid, gender, livetype, datasubtype, data)
                db.session.add(edd)
            gender = 0
            livetype = 2
            for ed in range(1, len(education_to_col) + 1):
                datasubtype = ed
                data = get_subdata(sheet, i + 118, education_to_col[ed])
                edd = EducationDetail(regid, gender, livetype, datasubtype, data)
                db.session.add(edd)
    db.session.commit()

def calcdemodata(datatype, filename):
    wb = open_workbook(filename)
    born = wb.sheets()[0]
    dead = wb.sheets()[4]
    data_born = {}
    for i in range(born.nrows):
        if born.cell(i,0).value in region_name_to_id:
            regid = region_name_to_id[born.cell(i,0).value]
            brn = born.cell(i,19).value
            data_born[regid] = brn 
    for i in range(dead.nrows):
        if dead.cell(i,0).value in region_name_to_id:
            regid = region_name_to_id[dead.cell(i,0).value]
            ded = dead.cell(i,19).value
            brn = data_born[regid]
            region = DemograghyRegion(regid, brn, ded) 
            db.session.add(region)
    db.session.commit()

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
                if datatype == 1:
                    calcedudata(datatype, filename)
                elif datatype == 2:
                    calcdemodata(datatype, filename)

    with open('include/adddata.html', 'r', encoding="utf-8") as page:
        data=page.read()
    return data

@app.route('/stat', methods = ["GET", "POST"])
def stat():
    if request.method == 'POST':
        regionid = int(request.form['regionid'])
        datatype = int(request.form['datatype'])
        ret = {}
        if datatype == 1:
            reg_info = EducationRegion.query.filter_by(id=regionid).first()
            ret['general'] = {}
            ret['general']['послевузовское'] = reg_info.postgraduate
            ret['general']['высшее'] = reg_info.higher
            ret['general']['неоконченное высшее'] = reg_info.higherip
            ret['general']['среднеe специальное'] = reg_info.middleprof
            ret['general']['начальное специальное'] = reg_info.basicprof
            ret['general']['среднее общее'] = reg_info.middlefull
            ret['general']['основное общее'] = reg_info.middlemain
            ret['general']['начальное'] = reg_info.basic
            ret['general']['без образования'] = reg_info.noeducation
            edu_detail = EducationDetail.query.filter_by(regionid=regionid).all()
            for j in range(len(edu_detail)):
                sub_dict = {}
                sub_dict['15-17'] = edu_detail[j].y1517
                sub_dict['18-19'] = edu_detail[j].y1819
                sub_dict['20-24'] = edu_detail[j].y2024
                sub_dict['25-29'] = edu_detail[j].y2529
                sub_dict['30-34'] = edu_detail[j].y3034
                sub_dict['35-39'] = edu_detail[j].y3539
                sub_dict['40-44'] = edu_detail[j].y4044
                sub_dict['45-49'] = edu_detail[j].y4549
                sub_dict['50-54'] = edu_detail[j].y5054
                sub_dict['55-59'] = edu_detail[j].y5559
                sub_dict['60-64'] = edu_detail[j].y6064
                sub_dict['65-69'] = edu_detail[j].y6569
                sub_dict['70 и старше'] = edu_detail[j].y70p
                eduname = eduid_to_name[edu_detail[j].datasubtype]
                if not eduname in ret:
                    ret[eduname] = {}
                if edu_detail[j].gender == 1:
                    ret[eduname]['М'] = sub_dict
                if edu_detail[j].gender == 2:
                    ret[eduname]['Ж'] = sub_dict
                if edu_detail[j].livetype == 1:
                    ret[eduname]['Город'] = sub_dict
                if edu_detail[j].livetype == 2:
                    ret[eduname]['Село'] = sub_dict
        elif datatype == 2:
            reg_info = DemograghyRegion.query.filter_by(id=regionid).first()
            ret['born'] = reg_info.born
            ret['dead'] = reg_info.dead
        return jsonify(ret)
    else:
        with open('include/stat.html', 'r', encoding="utf-8") as page:
            data=page.read()
        return data

@app.route('/report', methods = ["GET", "POST"])
def report():
    if request.method == 'POST':
        datatype = int(request.form['datatype'])
        ret = {}
        if datatype == 1:
            data = EducationRegion.query.all()
            for i in range(len(data)):
                good = data[i].postgraduate + data[i].higher + data[i].higherip + \
                    data[i].middleprof + data[i].basicprof + data[i].middlefull + \
                    data[i].middlemain
                bad = data[i].basic + data[i].noeducation
                ret[data[i].id] = bad/good * 100
        elif datatype == 2:
            data = DemograghyRegion.query.all()
            for i in range(len(data)):
                ret[data[i].id] = data[i].born/data[i].dead
        return jsonify(ret)


@app.route('/', methods = ["GET", "POST"])
def root():
    with open('include/index.html', 'r', encoding="utf-8") as page:
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

