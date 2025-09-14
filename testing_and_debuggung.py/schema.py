from pydantic import BaseModel
class itemschema(BaseModel):
    name: str
    color: str

class responseitemschema(itemschema):
    id: int
    class Config: 
        from_attributes = True