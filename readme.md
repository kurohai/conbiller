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
