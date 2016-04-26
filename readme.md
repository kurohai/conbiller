# ConBiller

> Because ConBill sucks

## Overview

This module is designed to help users fix common errors in ConBill flat files.

### commands to test
    python conbiller.py ./data/test-con-bill-file-01.txt

# ConBill DB

## Overview

A database for ConBill invoices. This will help fix ConBill invoicing errors by moving data from flat files to database.

### POA For Creation

1. Parse all fields into ConBillInvoice and ConBillProduct classes.
1. Add additional fields.
    1. Customer Name
    1. Major Customer Number
1. Make table with all fields.
    1. One table for invoice header details
    1. One table for product details
        1. Each product needs price_invoiced (original) and price_billed (updated).
        1. Each product needs pcode_invoiced and pcode_billed.
1. Make SQLA models for both classes
    1. Format ConBillInvoice class for SQLA model
    1. Format ConBillProduct class for SQLA model

### POA For Use

1. Put all invoices in db.
1. Find invoices with no problems to send.
1. Find invoices that only have price changes.
1. Find invoices that only have unauth products.
1. Find invoices with both


## TODO

- Migrate flat file field locations out of model to file_definition file



# ConBill Late Invoices Project

## Overview

Cleaning up the backlog of ConBill invoices while correcting errors.
The database will speed up the recovery by a considerable amount.

## Current Status

Parsing all files again to populate a database. Will be completed tonight.

## Next Steps

### Non Dollar Chain
Export one file for each major customer number for each day.

### Dollar Chain
> MCN 375, 368
1. Export one file for each customer number for each day/ week.
1. Change every price to ConBill's price if product is authorized.
1. If product is unauthorized leave price unchanged.



```
if brprice == cbprice:
    write line with brprice
elif brprice != cbprice and cbprice != 0.0:
    write line with cbprice
elif brprice != cbprice and cbprice == 0.0:
    write line with brprice
```




### SDMS Flat File Definitions

1. pepsi div id: 5
1. date: 6
1. filler zero: 3
1. customer number: 6
1. filler space: 12
1. invoice: 8
1. filler space: 23
1. filler zero: 7
1. filler space: 12
1. quantity: 5
1. credit or debit: 1
1. filler space: 9
1. filler zero: 5
1. filler space: 5
1. price: 7
1. filler zero: 24
1. brand: 4
1. filler zero: 7
1. pack id: 3
1. filler zero: 48
1. filler space: 30
