from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app=FastAPI()
class Userinput(BaseModel):
    age:int
    income:int
    state:str
    occupation:str

def get_connection():
    return psycopg2.connect(
        dbname="schemenavigator",
        user="postgres",
        password="8951245387",
        host="localhost",
        port="5432"
    )

@app.get("/")
def home():
    return{"message":"Scheme Navigator API is running"}

@app.post("/check-schemes")

def check_schemes(user:Userinput):
    conn=get_connection()
    cursor=conn.cursor()

    query="""
        SELECT name,benefit FROM schemenavigator
        WHERE state =%s
        AND occupation =%s
        AND income_limit>=%s;
    """
    cursor.execute(query,(user.state,user.occupation,user.income))
    results=cursor.fetchall()
    cursor.close()
    conn.close()
    schemes=[
        {"name":row[0],"benefit":row[1]}
        for row in results
    ]
    return {"eligible_schemes":schemes}
