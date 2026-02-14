from fastapi import FastAPI
from app.schemas import Userinput
from app.services.scheme_service import fetch_eligible_schemes
from app.services.ai_service import generate_ai_explaination
from fastapi.middleware.cors import CORSMiddleware



app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return{"message":"Scheme Navigator API is running"}

@app.post("/check-schemes")
def check_schemes(user:Userinput):
    try:
        schemes=fetch_eligible_schemes(user)
        enhanced_schemes=[]
        for scheme in schemes:
            ai_data=generate_ai_explaination(user,scheme)
            enhanced_schemes.append({**scheme,**ai_data})
        enhanced_schemes.sort(key=lambda x: x["score"], reverse=True)
        if enhanced_schemes:
            enhanced_schemes[0]["recommended"]=True

        if len(enhanced_schemes)==0:
            comparison_summary="No schemes matched your profile."
        

        elif len(enhanced_schemes) ==1:
            comparison_summary=(
                f"{enhanced_schemes[0]['name']} is the best availabe scheme based on your profile. "
            )
        else:
            top=enhanced_schemes[0]
            second=enhanced_schemes[1]
            comparison_summary=(
                f"{top['name']}ranks highest "
                f"compared to {second['name']}."
            )
        return {
            "eligible_schemes":enhanced_schemes,
            "comparison_summary":comparison_summary
        }
    except Exception as e:
        return {"error": str(e)}
   
