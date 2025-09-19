from pydantic import BaseModel
from typing import List

class Playlist(BaseModel):
    name : str
    songs: List[str] = []
