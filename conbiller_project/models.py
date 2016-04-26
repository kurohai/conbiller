from sqlalchemy import Column, ForeignKey, Float, Date
from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy import String, Text, BigInteger
from sqlalchemy.orm import relationship
from base import Base


class ConBillProduct(Base):
    """docstring for ConBillProduct"""
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=15), nullable=True)
    each_price = Column(Float)
    cbprice = Column(Float)
    quantity = Column(Integer)
    brand_id = Column(Integer)
    pack_id = Column(Integer)
    line = Column(String(length=15))
    cord = Column(String(length=15))
    pcode = Column(Integer)

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

        # super(ConBillProduct, self).__init__()


    def __repr__(self):
        return '{self.id}\t {self.pcode}'.format(self=self)


class ConBillInvoice(Base):
    """docstring for ConBillInvoice"""
    id = Column(Integer, primary_key=True, autoincrement=True)
    pepsi_div_id = Column(String(length=15), nullable=True)
    date = Column(String(length=15))
    cust_no = Column(String(length=15))
    invoice_no = Column(String(length=15))
    data = Column(Text)
    # products = relationship()
    total_invoice_price = Column(Float)
    final_billed_price = Column(Float)
    total_diff = Column(Float)
    major_cust_code = Column(Integer)

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

