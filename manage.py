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
def mcnexport(major_cust=None):

    if major_cust == None:
        print 'Major Customer Number Required'
        sys.exit(1)

    db = database_connection(dburi)
    # print(db.session)

    if int(major_cust) == 375:
        invoices = db.session.query(ConBillInvoice).filter(ConBillInvoice.major_cust_code == major_cust).all()
        print 'invoice count:', len(invoices)
        counter = 0
        for invoice in invoices:
            counter += 1
            if counter == 1:
                filename = '{cust}-0001.txt'.format(cust=invoice.major_cust_code)
            elif not counter % 1000:
                filename = '{cust}-{count}.txt'.format(cust=invoice.major_cust_code, count=counter)

            dirpath = './output/{mcn}'.format(mcn=invoice.major_cust_code)
            check_dir_exist(dirpath)
            filepath = os.path.join(dirpath, filename)
            products = db.session.query(ConBillProduct).filter(ConBillProduct.conbillinvoice_id == invoice.id).all()
            with open(filepath, 'ab') as f:
                for p in products:
                    if p.brand_id == 3863 and p.pack_id == 456:
                        p.brand_id = 3862
                        
                    f.write(p.export()+'\r\n')
                # # products = db.session.query(ConBillProduct).filter(ConBillProduct.conbillinvoice_id == invoice.id).all()
                # for p in products:
                #     f.write(p.export()+'\r\n')
        add_trailer(dirpath=dirpath)

    else:
        invoices = db.session.query(ConBillInvoice).filter(ConBillInvoice.major_cust_code == int(major_cust)).all()
        print 'invoice count:', len(invoices)
        if len(invoices) > 0:
            for invoice in invoices:
                dirpath = './output/{mcn}'.format(mcn=invoice.major_cust_code)
                check_dir_exist(dirpath)
                filename = '{cust}.txt'.format(cust=invoice.major_cust_code)
                filepath = os.path.join(dirpath, filename)
                products = db.session.query(ConBillProduct).filter(ConBillProduct.conbillinvoice_id == invoice.id).all()
                with open(filepath, 'ab') as f:
                    for p in products:
                        if p.brand_id == 3863 and p.pack_id == 456:
                            p.brand_id = 3862
                            
                        f.write(p.export()+'\r\n')
            add_trailer(dirpath=dirpath)




@manager.option('-d', '--directory', dest='dirpath', default=None)
def add_trailer(dirpath=None):
    files = os.listdir(dirpath)
    for file in files:
        filepath = os.path.join(dirpath, file)
        with open(filepath) as f:
            lines = f.readlines()
        if 'TRAILER' in lines[-1]:
            lines[-1] = 'TRAILER{0:09}{1}\r\n'.format(len(lines), ' '*214)
        else:
            lines.append('TRAILER{0:09}{1}\r\n'.format(len(lines)+1, ' '*214))
        with open(filepath, 'wb') as f:
            f.writelines(lines)


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
