from sqlmodel import SQLModel, Field 


class UserRegister(SQLModel , table=True):
    
    __tablename__="Users"

    id:int=Field(default=None,primary_key=True)
    firstname:str=Field(...,
            min_length=2,
            max_length=30,
            pattern="^[A-Za-z]+$"      
                        )
    lastname:str=Field(...,
            min_length=2,
            max_length=30,
            pattern="^[A-Za-z]+$"      
                        )
    username:str=Field(...,
             max_length=10,
             min_length=3,
             pattern="^[A-Za-z0-9]+$" ,
             unique=True         
                       )
    email: str = Field(index=True, unique=True)
    password_hash: str