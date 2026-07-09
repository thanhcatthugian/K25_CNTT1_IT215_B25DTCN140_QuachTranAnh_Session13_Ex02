from pydantic import BaseModel,Field,ConfigDict


class Items(BaseModel):
    dish_code:str = Field(...)
    dish_name:str = Field(...)
    calorie_count:int = Field(...)
    price:float = Field(...)
    status:str = Field(...)

class Response(BaseModel):
    id:int
    dish_code:str 
    dish_name:str
    calorie_count:int 
    price:float 
    status:str 
    model_config = ConfigDict(from_attributes=True)