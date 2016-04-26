from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from dicto import dicto
from base import Base
import time


def database_connection(dburi):

    db = dicto()
    db.base = Base()
    db.engine = create_engine(dburi)
    db.metadata = MetaData(bind=db.engine)
    db.session = Session(db.engine)

    db.db_session = scoped_session(
        sessionmaker(
            autocommit=True,
            autoflush=True,
            bind=db.engine
        )
    )

    db.base.query = db.db_session.query_property()
    from models import ConBillInvoice, ConBillProduct

    return db


def initdb(base):
    base.metadata.create_all(bind=engine)


def deldb(base):
    base.metadata.drop_all(bind=engine)
