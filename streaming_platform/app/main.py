from fastapi import FastAPI, Body, Depends,HTTPException
from fastapi.encoders import ENCODERS_BY_TYPE
from contextlib import asynccontextmanager
from bson import ObjectId

ENCODERS_BY_TYPE[ObjectId] = str

from app.database import mongo_database
from app.db_connection import ping_server
from app.schema import Playlist

@asynccontextmanager
async def lifespan(app : FastAPI):   
    await ping_server()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/song")
async def add_song(song: dict = Body(example = {"title" : "mysong", "artist" : "my artist"}), mongo_db = Depends(mongo_database)):
    await mongo_db.songs.insert_one(song)
    return {
        "message" : "song has been added",
        "id" : song["_id"]
    }

@app.get("/song/{song_id}")
async def get_song(song_id : str, mongo_db = Depends(mongo_database)):
    if not ObjectId.is_valid(song_id):
        raise HTTPException(status_code=400, detail="invalid song")
    song = await mongo_db.songs.find_one({"_id" : ObjectId(song_id)})
    
    if not song:
        raise HTTPException(status_code=404,detail= "song not found")
    return song

@app.delete("/song/{song_id}")
async def delete_song(song_id : str, mongo_db = Depends(mongo_database)):
    if not ObjectId.is_valid(song_id):
        return None
    result = await mongo_db.songs.delete_one({"_id" : ObjectId(song_id)})
    if result.deleted_count == 1:
        return { "message" : "songs deleted succesfully"}
    else:
        raise HTTPException (status_code=404, detail="song not found")
    
@app.post("/plalist")
async def create_playlist(playlist: Playlist = Body(
    example={
        "name" : "My_playlist",
        "songs" : ["song_id"]
    }
), db = Depends(mongo_database)):
    result = await db.playlist.insert_one(playlist.model_dump())
    return {
        "message" :"Playlist created succesful",
        "id" : str(result.inserted_id) 
    }

@app.get("/playlist/{playlist_id}")
async def get_playlist(playlist_id : str, db = Depends(mongo_database)):
    if not ObjectId.is_valid(playlist_id):
        raise HTTPException(status_code=404, detail="not found")
    playlist = await db.playlist.find_one({"_id" : ObjectId(playlist_id)})
    song = await db.songs.find_one({
        "_id": {
            "$in" : [
                ObjectId(song_id)
                for song_id in playlist["songs"]
            ]
        }
    })
    return {
        "name" : playlist["name"],
        "song" : song
    }