
from util import

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
                self.db.session.add(p)
                self.db.session.commit()
