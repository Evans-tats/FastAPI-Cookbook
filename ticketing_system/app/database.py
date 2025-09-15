from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer,String,Float,Boolean

class Base(DeclarativeBase):
    pass

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer,primary_key = True, index = True)
    price = Column(Float, index=True, nullable= True)
    show = Column(String)
    user = Column(String)
    sold = Column(Boolean, default=False)

