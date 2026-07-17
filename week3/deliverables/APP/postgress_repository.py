from sqlmodel import Session,select

from APP.model import UserRegister
from APP.repository import UserRepository



class PostgresRepository(UserRepository):
    def __init__(self,session:Session):

        self.session=session

    def add(self, user:UserRegister) ->UserRegister:
        self.session.add(user)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        self.session.refresh(user)
        return user
    

    def get_by_name(self, username:str):
        statement=select(UserRegister).where(UserRegister.username == username)
        return self.session.exec(statement).first()
    
    def get_by_email(self, email:str):
        statement=select(UserRegister).where(UserRegister.email == email)
        return self.session.exec(statement).first()


