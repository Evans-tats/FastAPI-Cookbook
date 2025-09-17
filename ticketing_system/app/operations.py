from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,delete
from sqlalchemy.orm import selectinload

from .database import Ticket,Event
from .schema import TicketCreate, TicketRead, EventCreate, EventRead

async def create_ticket(ticket: TicketCreate, db_session: AsyncSession):
    new_ticket = Ticket(
        price=ticket.price,
        name=ticket.name,
        event_id=ticket.event_id
    )
    async with db_session.begin():
        db_session.add(new_ticket)
        await db_session.flush()
        
    await db_session.refresh(new_ticket)

    # Eager load event + details
    result = await db_session.execute(
        select(Ticket)
        .options(
            selectinload(Ticket.event),       # Load event for event_name
            selectinload(Ticket.details)     # Load details
        )
        .where(Ticket.id == new_ticket.id)
    )
    ticket_with_rels = result.scalar_one()

    # Manually map event_name since TicketRead expects it
    return ticket_with_rels

async def create_event(event: EventCreate, db_session : AsyncSession):
    new_event = Event(event_name= event.event_name, max_ticket = event.max_ticket)
    async with db_session.begin():
        db_session.add(new_event)
        await db_session.flush()
    await db_session.refresh(new_event)
    result = await db_session.execute(
    select(Event).options(selectinload(Event.tickets)).where(Event.id == new_event.id)
    )
    new_event = result.scalar_one()
    return EventRead.model_validate(new_event)

async def get_ticket(ticket_id : int, db_session : AsyncSession):
    query = (select(Ticket).options(selectinload(Ticket.details)).where(Ticket.id == ticket_id))
    async with db_session as session:
        result = await session.execute(query)
        ticket = result.scalars().first()
    if not ticket:
        return None
    return ticket

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