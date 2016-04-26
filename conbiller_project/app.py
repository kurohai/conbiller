# -*- coding: utf-8 -*-
# @Author: root
# @Date:   2016-04-25 18:23:33
# @Last Modified by:   root
# @Last Modified time: 2016-04-25 18:32:07

from flask import Flask
import settings

flasktemplate = Flask(__name__)
flasktemplate.appname = settings.appname
flasktemplate.appnamed = settings.appnamed
flasktemplate.config.SECRET_KEY = settings.SECRET_KEY
flasktemplate.config.SESSION_PROTECTION = settings.SESSION_PROTECTION

