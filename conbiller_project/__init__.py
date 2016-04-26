# -*- coding: utf-8 -*-
# @Author: root
# @Date:   2016-04-25 18:13:56
# @Last Modified by:   root
# @Last Modified time: 2016-04-25 22:20:37

from dicto import dicto
from pprint import pprint

from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, inspect, MetaData
import datetime
import os
import logging
from flask import Flask
from flask.ext.admin import Admin
from sqlalchemy.ext.declarative import *

import settings
from database import database_connection

# settings
pwd = settings.pwd
appname = settings.appname
appnamed = settings.appnamed
secret_key = settings.secret_key
# dbpath = settings.dbpath
dburi = settings.dburi

# logging
log = logging.getLogger(__name__)
handler = logging.StreamHandler()
log.level = logging.DEBUG
handler.setLevel = logging.DEBUG
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

flasktemplate = Flask(__name__)

from models_old import ConBillInvoiceMapper, ConBillProductMapper

db = database_connection(dburi)
from models import *
