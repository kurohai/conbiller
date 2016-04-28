from sqlalchemy import Column, ForeignKey, Float, Date
from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy import String, Text, BigInteger
from sqlalchemy.orm import relationship
from base import Base


class ConBillProduct(Base):
    """docstring for ConBillProduct"""
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=True)
    each_price = Column(Float)
    cbprice = Column(Float)
    quantity = Column(Integer)
    brand_id = Column(Integer)
    pack_id = Column(Integer)
    line = Column(Text)
    cord = Column(String(length=15))
    pcode = Column(Integer)
    conbillinvoice_id = Column(Integer, ForeignKey('conbillinvoice.id'))

    def __init__(self, product=None):
        if product != None:
            self.name = product.name
            self.each_price = product.each_price
            self.cbprice = product.cbprice
            self.quantity = product.quantity
            self.brand_id = product.brand_id
            self.pack_id = product.pack_id
            self.line = product.line
            self.cord = product.cord
            self.pcode = product.pcode

    def export(self):
        bill_price = int()
        if self.conbillinvoice.major_cust_code == 375:
            if self.each_price == self.cbprice:
                # print 'both equal'
                bill_price = self.each_price
            elif self.each_price != self.cbprice and self.cbprice != 0.0:
                # print 'not equal auth'
                # print self.cbprice
                bill_price = self.cbprice
            elif self.each_price != self.cbprice and self.cbprice == 0.0:
                # print 'not equal not auth'
                bill_price = self.each_price
        else:
            bill_price = self.each_price
        bill_price = '{0:.2f}'.format(bill_price)
        # print 'formatted:', bill_price
        bill_price = str(bill_price).replace('.', '').zfill(7)
        # while len(bill_price) < 7:
        #     bill_price

        return product_line_template.format(
                self=self,
                bill_price=bill_price,
            )


    def __repr__(self):
        return '<ConBillProduct object pcode:{self.pcode}>'.format(self=self)


class ConBillInvoice(Base):
    """docstring for ConBillInvoice"""
    id = Column(Integer, primary_key=True, autoincrement=True)
    pepsi_div_id = Column(String(length=15), nullable=True)
    date = Column(String(length=15))
    cust_no = Column(String(length=15))
    invoice_no = Column(String(length=15))
    data = Column(Text)

    conbillproducts = relationship(
        'ConBillProduct',
        backref='conbillinvoice',
        primaryjoin="ConBillInvoice.id==ConBillProduct.conbillinvoice_id",
    )

    total_invoice_price = Column(Float)
    final_billed_price = Column(Float)
    total_diff = Column(Float)
    major_cust_code = Column(Integer)

    # def export(self):
    #     return product_line_template.format(
    #             self=self,
    #             bill_price=bill_price,
    #         )

    def __init__(self, invoice=None):
        if invoice != None:
            self.pepsi_div_id = invoice.pepsi_div_id
            self.date = invoice.date
            self.cust_no = invoice.cust_no
            self.invoice_no = invoice.invoice_no
            self.data = ''.join(invoice.data)
            self.total_invoice_price = invoice.total_invoice_price
            self.total_diff = invoice.total_diff
            self.major_cust_code = invoice.major_cust_code

    def __repr__(self):
        return '<ConBillInvoice object invoice:{self.invoice_no}>'.format(self=self)


product_line_template = """{self.conbillinvoice.pepsi_div_id:5}\
{self.conbillinvoice.date:6}\
000\
{self.conbillinvoice.cust_no:6}\
            \
{self.conbillinvoice.invoice_no:8}\
                       \
0000000\
            \
{self.quantity:05}\
{self.cord}\
         \
00000\
     \
{bill_price}\
000000000000000000000000\
{self.brand_id:04}\
000000\
{self.pack_id:0>4}\
000000000000000000000000000000000000000000000000\
                              """
