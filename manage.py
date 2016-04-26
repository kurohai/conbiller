import os
import cherrypy
from cherrypy import wsgiserver
from cherrypy.process.plugins import Daemonizer,PIDFile
from flask.ext.script import Manager
from conbiller_project import flasktemplate, database_connection, dburi
from pprint import pprint

manager = Manager(flasktemplate)


@manager.command
def db():
    db = database_connection(dburi)
    db.base.metadata.drop_all(bind=db.engine)
    db.base.metadata.create_all(bind=db.engine)
    data(db)


@manager.command
def data(db):
    pass


@manager.command
def quick():
    d = wsgiserver.WSGIPathInfoDispatcher({'/': flasktemplate})
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 80), d, server_name=flasktemplate.appname, )
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


@manager.command
def go():
    flasktemplate.run(debug=True, host='0.0.0.0', port=80)


if __name__ == '__main__':
    manager.run()
