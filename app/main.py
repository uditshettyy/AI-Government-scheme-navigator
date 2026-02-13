from fastapi import FastAPI
from app.schemas import Userinput
from app.services.scheme_service import fetch_eligible_schemes

app=FastAPI()



@app.get("/")
def home():
    return{"message":"Scheme Navigator API is running"}

@app.post("/check-schemes")

def check_schemes(user:Userinput):
    schemes=fetch_eligible_schemes(user)
    return {"eligible_schemes":schemes}
   
