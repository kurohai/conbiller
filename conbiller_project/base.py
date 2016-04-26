from sqlalchemy.ext.declarative import as_declarative, declared_attr
from dicto import dicto



@as_declarative()
class Base(dicto):

    def __hash__(self):
        return hash(self.id)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

