from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker


SQLALCHEMY_DATABASE_URL = ("sqlite+aiosqlite:///./app/database.db")

def get_engine():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo =True)
    return engine

asyncSessionLocal = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=get_engine(),
    class_=AsyncSession
)
async def get_db_session():
    async with asyncSessionLocal() as session:
        yield session

