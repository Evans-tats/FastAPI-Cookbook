from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# ---------------- Ticket Details ----------------
class TicketDetailsBase(BaseModel):
    seat: Optional[str] = None
    ticket_type: Optional[str] = None


class TicketDetailsCreate(TicketDetailsBase):
    pass


class TicketDetailsRead(TicketDetailsBase):
    id: int
    ticket_id: int
    model_config = ConfigDict(from_attributes=True)


# ---------------- Ticket ----------------
class TicketBase(BaseModel):
    name: str
    price: float


class TicketCreate(TicketBase):
    event_id: int
    details: Optional[TicketDetailsCreate] = None

class EventMini(BaseModel):
    id: int
    event_name: str
    max_ticket: int

    model_config = ConfigDict(from_attributes=True)


class TicketRead(TicketBase):
    id: int
    sold: bool
    details: Optional[TicketDetailsRead] = None
    event: EventMini   # prevents circular loop
    model_config = ConfigDict(from_attributes=True)

# ---------------- Event ----------------
class EventBase(BaseModel):
    event_name: str
    max_ticket: int


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int
    tickets: List[TicketRead] = []
    model_config = ConfigDict(from_attributes=True)
