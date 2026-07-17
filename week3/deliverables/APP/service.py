# from sqlalchemy.orm import Session
from sqlmodel import select,Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException,status
from APP.security import verify_password

from APP.schema  import SignupUser,UserBase
from APP.model import UserRegister
from APP.security import hash_password
from APP.repository import UserRepository



class RegisterService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    

    def add(self,user_create:SignupUser)->UserBase:
         
        hashed_pwd = hash_password(user_create.password)

        new_user = UserRegister(
        firstname=user_create.firstname,
        lastname=user_create.lastname,
        username=user_create.username,
        email=user_create.email,
        password_hash=hashed_pwd  
        )

        try:
            self.repo.add(new_user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already registered",
            )

        return UserBase.model_validate(new_user)

    def get_user(self, username: str) -> UserBase:
        user = self.repo.get_by_name(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserBase.model_validate(user)



    def login(self, login_data):

        user = self.repo.get_by_email(login_data.email)

        if not user:
             raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(login_data.password, user.password_hash):
              raise HTTPException(status_code=401, detail="Invalid password")

        return {"message": "Login successful"}