from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

from APP.database import get_session
from APP.service import RegisterService
from APP.postgress_repository import PostgresRepository

SessionDep = Annotated[Session, Depends(get_session)]

def get_register_service(session: Session = Depends(get_session)):
    repo = PostgresRepository(session)
    return RegisterService(repo)

ServiceDep = Annotated[
    RegisterService,
    Depends(get_register_service),
]