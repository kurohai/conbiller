# import sys
# from database import *
# from models import *
# from models_old import ConBillInvoice
import csv
from dicto import dicto


def get_conbill_prices(infile):
    cbprices = list()
    infile = './data/dollar-price.csv'
    with open(infile) as f:
        lines = csv.reader(f, dialect='excel')
        for line in lines:
            p = dicto()
            p.brand_id = line[1]
            p.pack_id = line[2]
            p.price = line[4]
            p.name = line[0]
            cbprices.append(p)
    return cbprices


def make_invoice(lines):
    from models_old import ConBillInvoiceMapper
    return ConBillInvoiceMapper(lines)


def separate_invoices(lines):
    invoices = list()
    last_inv = str()
    line_collect = list()
    for k, line in enumerate(lines):
        index = k
        # if 'TRAILER' not in line:
        this_inv = line[33:41]
        if not this_inv == last_inv:
            if not last_inv == '':
                i = make_invoice(line_collect)
                invoices.append(i)
            index = k
            last_inv = this_inv
            line_collect = list()
            line_collect.append(line)
        else:
            line_collect.append(line)
    return invoices


def get_invoices(infile):
    with open(infile) as f:
        # separate invoices here
        lines = f.readlines()
    return separate_invoices(lines)

def split_by_major_cust(infile):
    invoices = get_invoices(infile)
    print 'found {0} invoices'.format(len(invoices))
    print 'writing to files...'
    for invoice in invoices:
        cust = arcustmr.query.filter(arcustmr.cust_no == invoice.cust_no).first()
        filename = 'output/{0}.txt'.format(cust.major_cust_code)
        with open(filename, 'a') as f:
            # f.write('{0}\t{1}\t{2}\n'.format(cust.major_cust_code,cust.cust_no,invoice.invoice_no))
            for line in invoice.data:
                f.write('{0}'.format(line))
        # print cust.major_cust_code
    print 'Done!'
