from sqlmodel import create_engine
from sqlmodel import Session
from sqlmodel import SQLModel

from APP.model import UserRegister
from  APP.config import settings

engine=create_engine(
    url=settings.POSTGRES_URL,
    echo=True,
)

def create_table():
    SQLModel.metadata.create_all(bind=engine)

def get_session():
    with Session(engine) as session:
        yield session