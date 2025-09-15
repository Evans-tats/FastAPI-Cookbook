from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from .db_connection import get_engine, get_db_session
from .database import Base
from .operations import create_ticket,get_ticket, update_price_of_ticket, delete_ticket
from .schema import Ticket_schema, returnTicket_schema


@asynccontextmanager
async def lifespan(app : FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.post("/ticket", status_code=status.HTTP_201_CREATED)
async def create_ticket_route(ticket: Ticket_schema,db_session: AsyncSession = Depends(get_db_session)):
    ticket = await create_ticket(ticket,db_session)
    return returnTicket_schema.model_validate(ticket)

@app.get("/ticket/{ticket_id}",status_code=status.HTTP_200_OK)
async def get_ticket_route(ticket_id : int, db_session: AsyncSession = Depends(get_db_session)):
    ticket = await get_ticket(ticket_id, db_session)
    if ticket is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="the requested ticket is not availabe")
    return returnTicket_schema.model_validate(ticket)

@app.post("/ticket/update/{ticket_id}")
async def update_ticket_price_route(ticket_id : int, new_price: int, db_session : AsyncSession = Depends(get_db_session)):
    ticket_update_status = await update_price_of_ticket(ticket_id,new_price, db_session)
    if ticket_update_status is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the ticket you seek is not in our system, please confirm")
    if ticket_update_status is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "update failed, contact customer support")
    return{
        "message": "succesfully updated the price"
    }
@app.delete("/ticket/{ticket_id}",status_code=status.HTTP_200_OK)
async def delete_ticket_route(ticket_id :int , db_session : AsyncSession = Depends(get_db_session)):
    result = await delete_ticket(ticket_id, db_session)
    if result is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ticket not found")
    return {
        "message": f"succesfully deleted tiscket with id {ticket_id}"
    }