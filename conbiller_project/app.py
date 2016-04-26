# -*- coding: utf-8 -*-
# @Author: root
# @Date:   2016-04-25 18:23:33
# @Last Modified by:   kurohai
# @Last Modified time: 2016-04-26 08:15:34

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from database import database_connection
import settings
from models import ConBillProduct, ConBillInvoice

flaskapp = Flask(__name__)
flaskapp.appname = settings.appname
flaskapp.appnamed = settings.appnamed
flaskapp.config.SECRET_KEY = settings.secret_key
flaskapp.config.SESSION_PROTECTION = settings.session_protection


flasktemplate = flaskapp
db = database_connection(settings.dburi)

admin = Admin(flaskapp, name='conbiller', template_mode='bootstrap3')
admin.add_view(ModelView(ConBillProduct, db.session))
admin.add_view(ModelView(ConBillInvoice, db.session))
