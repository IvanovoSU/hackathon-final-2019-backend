# -*- coding: utf-8 -*-
from main import db
from main import User
db.create_all()
admin = User(1, 'admin', 'admin')
db.session.add(admin)
db.session.commit()
