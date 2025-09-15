from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,delete

from .database import Ticket
from .schema import Ticket_schema, returnTicket_schema

async def create_ticket(ticket: Ticket_schema, db_session : AsyncSession):
    ticket = Ticket(price=ticket.price, show = ticket.show, user=ticket.user)
    async with db_session.begin():
        db_session.add(ticket)
        await db_session.flush()
    await db_session.refresh(ticket)
    return returnTicket_schema.model_validate(ticket)

async def get_ticket(ticket_id : int, db_session : AsyncSession) -> returnTicket_schema | None : 
    query = (select(Ticket).where(Ticket.id == ticket_id))
    async with db_session as session:
        result = await session.execute(query)
        ticket = result.scalars().first()
    if not ticket:
        return None
    return returnTicket_schema.model_validate(ticket)

async def update_price_of_ticket(ticket_id : int, new_price : float, db_session : AsyncSession):
    result = await get_ticket(ticket_id, db_session)
    if result is None:
        return None
    query = (
    update(Ticket)
    .where(Ticket.id == ticket_id)
    .values(price=new_price)
    .execution_options(synchronize_session="fetch")
)
    async with db_session.begin():
        ticket_update = await db_session.execute(query)

    if ticket_update.rowcount == 0:
        return False
    return True

async def delete_ticket(ticket_id :int, db_session :AsyncSession):
    query = (delete(Ticket).where(Ticket.id == ticket_id))
    async with db_session.begin():
        result = await db_session.execute(query)
    if result.rowcount == 0:
        return False
    return True