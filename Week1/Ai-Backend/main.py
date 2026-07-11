#importing necessary library "FastAPI" from "fastapi" 
from fastapi import FastAPI

# Creating "FastAPI" instance
app = FastAPI(
    title="My API"
)

# <------------ Creating Endpoint ---------->

# ------ Root endpoint ---------
@app.get("/")
def root():
    return {
        "message":"this is Root"
    }

# ----------home endpoint -------
@app.get("/home")
def get_home():
    return {
        "message":"Welcome to home"
    }


#=================================================#
    """
    RUN this RUNNING THIS COMMAND : uvicorn main:app --reload
    Test it :putting localhost address on browser 
    
    """
