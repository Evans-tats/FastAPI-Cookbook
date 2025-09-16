from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer,String,Float,Boolean,ForeignKey
from typing import List
class Base(DeclarativeBase):
    pass

class Ticket(Base):
    __tablename__ = "tickets"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    price : Mapped[float | None] = mapped_column(Float, nullable=True)
    name : Mapped[str] = mapped_column(String)
    sold : Mapped[Boolean] = mapped_column(Boolean, default= False)
    event_id : Mapped[int] = mapped_column(ForeignKey("events.id"))
    
    details: Mapped["TicketDetails"] = relationship(back_populates="ticket", uselist=False)
    event : Mapped["Event | None"] = relationship(back_populates="tickets")

class TicketDetails(Base):
    __tablename__ = "ticket_details"
    id : Mapped[int] = mapped_column(Integer,primary_key=True)
    ticket_id : Mapped[int] = mapped_column(ForeignKey("tickets.id"), unique=True) 
    seat : Mapped[str | None] = mapped_column(String, nullable=True)
    ticket_type : Mapped[str | None] = mapped_column(String, nullable=True)

    ticket : Mapped["Ticket"] = relationship(back_populates="details")

class Event(Base):
    __tablename__= "events"

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    event_name : Mapped[str] = mapped_column(String)
    max_ticket : Mapped[int] = mapped_column(Integer)
    tickets : Mapped[List["Ticket"]] = relationship(back_populates="event")
    