from motor.motor_asyncio import AsyncIOMotorClient
import logging

MONGO_CLIENT = AsyncIOMotorClient("mongodb://localhost:27017")

logger = logging.getLogger("uvicorn.error")

async def ping_server():
    try:
        await MONGO_CLIENT.admin.command("ping")
        logger.info("connected to MongDB")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {e}")
        raise e
