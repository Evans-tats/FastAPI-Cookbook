from app.db_connection import MONGO_CLIENT

database = MONGO_CLIENT.beat_streaming
def mongo_database():
    return database