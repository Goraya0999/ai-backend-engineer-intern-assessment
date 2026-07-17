from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from .schema import SignupUser,LoginUser
from APP.dependencies import ServiceDep
from APP.database import create_table



app=FastAPI(
    title="Fly Rank Intern Task"
)
@app.on_event("startup")
def on_startup():
    create_table()





@app.get("/home")
def home():
    return {
        "message":"welcome to home"
    }


@app.post("/signup")
def signup(register:SignupUser,service:ServiceDep):
    return service.add(register)



@app.post("/login")
def loginUser(lgin:LoginUser, service:ServiceDep):
    return service.login(lgin)


@app.get("/users/{username}")
def get_user(username: str, service: ServiceDep):
    return service.get_user(username)

### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
