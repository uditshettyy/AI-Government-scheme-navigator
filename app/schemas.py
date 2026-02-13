from pydantic import BaseModel

class Userinput(BaseModel):
    age:int
    income:int
    state:str
    occupation:str
