from pydantic import BaseModel, ConfigDict

class Ticket_schema(BaseModel):
    price : float
    user : str
    show: str

class returnTicket_schema(Ticket_schema):
    id : int
    model_config = ConfigDict(from_attributes=True)

