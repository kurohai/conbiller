# -*- coding: utf-8 -*-
# @Author: root
# @Date:   2016-04-25 18:20:17
# @Last Modified by:   root
# @Last Modified time: 2016-04-25 22:53:22

import unittest
from pprint import pprint

import conbiller_project
from conbiller_project.base import Base
from conbiller_project import util
from dicto import dicto


from sqlalchemy.engine import Engine
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session


class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.db = conbiller_project.database.database_connection(conbiller_project.settings.dburi)

    def testDatabaseConnection(self):

        self.assertIsInstance(self.db, dicto)
        self.assertIsInstance(self.db.base, Base)
        self.assertIsInstance(self.db.engine, Engine)
        self.assertIsInstance(self.db.metadata, MetaData)
        self.assertIsInstance(self.db.session, Session)
        self.assertIsInstance(self.db.db_session, scoped_session)

        # need to find a way to test this
        # self.assertIsInstance(self.db.base.query, dict)


class ModelTestCase(unittest.TestCase):

    def setUp(self):
        self.db = conbiller_project.database.database_connection(conbiller_project.settings.dburi)
        self.test_file_01 = './test-data/test-con-bill-file-01.txt'
        with open(self.test_file_01) as f:
            self.test_invoice_01 = f.readlines()


    def testInvoiceParser(self):
        invoices = util.get_invoices(self.test_file_01)
        self.assertIsInstance(invoices, list)
        for invoice in invoices:
            self.assertIsInstance(invoice, conbiller_project.ConBillInvoiceMapper)
            d = conbiller_project.ConBillInvoice(invoice)
            self.db.session.add(d)
            self.db.session.commit()

            for prod in invoice.products:
                p = conbiller_project.ConBillProduct(prod)
                p.conbillinvoice_id = d.id
                print p.conbillinvoice_id

                self.db.session.add(p)
                self.db.session.commit()



if __name__ == '__main__':
    unittest.main()
