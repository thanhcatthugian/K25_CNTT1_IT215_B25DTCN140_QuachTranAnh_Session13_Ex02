from pydantic import BaseModel,Field,ConfigDict

class Slots(BaseModel):
    slot_number:str = Field(...)
    room_size :str = Field(...)
    price_per_day:float = Field(...)
    status:str = Field(...)


class Response(BaseModel):
    id:int
    slot_number:str 
    room_size :str 
    price_per_day:float 
    status:str 
    model_config = ConfigDict(from_attributes=True)