from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, ForeignKey, Float, Date
from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy import String, Text, BigInteger
import csv
from base import Base
from reflection import franchise_product, arcustmr
from dicto import dicto
from util import get_conbill_prices


class ConBillProductMapper(dicto):
    def __init__(self, line):
        self.each_price = float()
        self.quantity = int()
        self.brand_id = str()
        self.pack_id = str()
        self.line = line
        self.cord = str()
        self.parse_line()
        self.cbprice = float()
        self.name = str()

        self.pcode = self._get_pcode()
        self._get_cb_price()

    def parse_line(self):
        self.cord = self.line[87:88]
        self.quantity = int(self.line[82:87])
        self.each_price = float('{0}.{1}'\
            .format(self.line[107:112], self.line[112:114]))
        self.brand_id = self.line[138:142]
        self.pack_id = self.line[147:152]

    @property
    def total_line_price(self):
        if self.cord == 'S':
            return float(self.quantity * self.each_price)
        elif self.cord == 'C':
            return 0 - float(self.quantity * self.each_price)

    def _get_pcode(self):
        # prod = franchise_product.query.\
        #     filter(franchise_product.franc_brand_code == int(self.brand_id), franchise_product.conbil_pack_code == int(self.pack_id)).\
        #     first()
        prod = franchise_product.query.\
            filter(franchise_product.franc_brand_code == int(self.brand_id)).\
            filter(franchise_product.conbil_pack_code == int(self.pack_id)).\
            first()
        if prod is not None:
            return prod.prod_code

    def export(self):
        return '{0},{1},{2},{3}'.format(
                                        self.pcode,
                                        self.name,
                                        self.each_price,
                                        self.cbprice,
                                        )

    def _get_cb_price(self):
        for d in get_conbill_prices(1):
            if int(d.brand_id) == int(self.brand_id) and int(d.pack_id) == int(self.pack_id):
                self.cbprice = float(d.price)
                self.name = d.name.strip()
                # print 'found: ', d.name, d.brand_id, d.pack_id
                break

    @property
    def check_price(self):
        if self.each_price != self.cbprice:
            return False
        else:
            return True


class ConBillInvoiceMapper(dicto):

    def __init__(self, lines):
        """lines = list of all lines containing one invoice"""
        self.pepsi_div_id = str()
        self.date = str()
        self.filler = str()
        self.cust_no = str()
        self.invoice_no = str()
        self.data = lines
        self.products = list()
        self.total_diff = float()
        self._parse_lines(lines)
        self.report()

    @property
    def total_invoice_price(self):
        total = float()
        for prod in self.products:
            if prod.cord == 'S':
                total += prod.each_price
            if prod.cord == 'C':
                total -= prod.each_price
        return total

    def _update_total_price(self, price):
        pass

    @property
    def major_cust_code(self):
        cust = arcustmr.query.filter(arcustmr.cust_no == self.cust_no).first()
        return cust.major_cust_code

    def report(self):
        for prod in self.products:
            if not prod.check_price:
                if prod.cord == 'S' and prod.each_price > prod.cbprice:
                    self.total_diff -= (prod.each_price - prod.cbprice) * prod.quantity


                if prod.cord == 'S' and prod.each_price < prod.cbprice:
                    self.total_diff += (prod.cbprice - prod.each_price) * prod.quantity

                if prod.cord == 'C' and prod.each_price > prod.cbprice:
                    self.total_diff -= (prod.each_price - prod.cbprice) * prod.quantity

                if prod.cord == 'C' and prod.each_price < prod.cbprice:
                    self.total_diff += (prod.cbprice - prod.each_price) * prod.quantity

                    
                if prod.cord == 'S':
                    lost = (prod.cbprice - prod.each_price) * prod.quantity

                print '{0},{1},{2},{3},{4}'.format(
                                        prod.pcode,
                                        prod.name,
                                        prod.each_price,
                                        prod.cbprice,
                                        self.total_diff,
                                        )

    def _parse_lines(self, lines):
        for line in lines:
            if 'TRAILER' not in line:
                try:
                    self._parse_line(line)
                    self._parse_product(line)
                except ValueError as e:
                    pass

    def _parse_line(self, line):
        self.pepsi_div_id = line[0:5]
        self.date = line[5:11]
        self.filler = line[11:14]
        self.cust_no = line[14:20]
        self.invoice_no = line[32:40]

    def _parse_product(self, line):
        p = ConBillProductMapper(line)
        self.products.append(p)

    def update_total_price(self, price):
        self.total_invoice_price += price

    def __repr__(self):
        return 'pepsi_div_id = {div}\ndate = {date}\ncust_no = {c}\ninvoice_no = {i}'.format(
                                        div = self.pepsi_div_id,
                                        date = self.date,
                                        c = self.cust_no,
                                        i = self.invoice_no,
                                        )


# def get_major_cust_no(cust_no):
#     cust = arcustmr.query.filter(arcustmr.cust_no == cust_no).first()
#     return cust.major_cust_code
