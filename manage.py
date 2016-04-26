import os
import cherrypy
from cherrypy import wsgiserver
from cherrypy.process.plugins import Daemonizer,PIDFile
from flask.ext.script import Command, Manager, Option
from conbiller_project import flaskapp, database_connection, dburi
from conbiller_project import ConBillProduct, ConBillInvoice
from conbiller_project.util import get_invoices
from pprint import pprint

manager = Manager(flaskapp)



@manager.option('-f', '--file', dest='infile', default=None)
def process(infile=None):
    db = database_connection(dburi)
    invoices = get_invoices(infile)
    for invoice in invoices:
        d = ConBillInvoice(invoice)
        db.session.add(d)
        db.session.commit()

        for prod in invoice.products:
            p = ConBillProduct(prod)
            p.conbillinvoice_id = d.id
            db.session.add(p)
            db.session.commit()


@manager.option('-m', '--mcn', dest='major_cust', default=None)
@manager.option('-d', '--date', dest='target_date', default=None)
def mcnexport(major_cust=None, target_date=None):

    if major_cust == None:
        print 'Major Customer Number Required'
        sys.exit(1)

    db = database_connection(dburi)
    # print(db.session)

    if target_date == None:
        invoices = db.session.query(ConBillInvoice).filter(ConBillInvoice.major_cust_code == major_cust).all()
        # print 'invoice count', len(invoices)

        for invoice in invoices:
            dirpath = './output/{mcn}'.format(mcn=invoice.major_cust_code)
            check_dir_exist(dirpath)
            filename = '{cust}.txt'.format(cust=invoice.cust_no)
            filepath = os.path.join(dirpath, filename)

            with open(filepath, 'a') as f:
                products = db.session.query(ConBillProduct).filter(ConBillProduct.conbillinvoice_id == invoice.id).all()
                for p in products:
                    f.write(p.export()+'\n')



# @manager.option('-c', '--customer-number', dest='customer_number', default=None)
# @manager.option('-d', '--date', dest='target_date', default=None)
# def cnexport(major_cust=None, customer_number=None, target_date=None):
#     pass

# @manager.option('-m', '--mcn', dest='major_cust', default=None)
# @manager.option('-c', '--customer-number', dest='customer_number', default=None)
# @manager.option('-d', '--date', dest='target_date', default=None)
# def dateexport(major_cust=None, customer_number=None, target_date=None):
#     pass


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
    d = wsgiserver.WSGIPathInfoDispatcher({'/': flaskapp})
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 80), d, server_name=flaskapp.appname, )
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()


@manager.command
def go():
    flaskapp.run(debug=True, host='0.0.0.0', port=80)

def check_dir_exist(dirpath):
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)

if __name__ == '__main__':
    manager.run()
