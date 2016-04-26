from models import ConBillInvoice
import logging
import sys
from util import get_invoices
# from .conbiller_project import db
# need database connection import

log = logging.getLogger(__name__)
handler = logging.StreamHandler()
log.level = logging.DEBUG
handler.setLevel = logging.DEBUG
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


log.info('app started!')


def main(infile):
    log.info('main started!')
    invoices = get_invoices(infile)
    print len(invoices)
    for i in invoices:
        d = ConBillInvoice(i)

        session.add(d)
        session.commit()


if __name__ == '__main__':
    main(sys.argv[1])
