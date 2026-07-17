import re
from pydantic import BaseModel ,EmailStr,Field,field_validator

class UserBase(BaseModel):
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

class SignupUser(UserBase):
    username:str=Field(...,
             max_length=10,
             min_length=3,
             pattern="^[A-Za-z0-9]+$"          
                       )
    email:EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        pattern = r"^(?=(?:.*[a-z]){4,})(?=(?:.*[A-Z]){3,})(?=(?:.*\d){3,})(?=(?:.*[^A-Za-z0-9]){2,}).{12,}$"
        
        if not re.match(pattern, value):
            raise ValueError(
                "Password must have: 4 lowercase, 3 uppercase, 3 digits, 2 special chars, min length 12"
            )
        return value
    
class LoginUser(BaseModel):
    email:EmailStr
    password:str