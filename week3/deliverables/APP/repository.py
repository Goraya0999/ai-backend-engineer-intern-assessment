from abc import ABC,abstractmethod
from APP.model import UserRegister

class UserRepository(ABC):
    @abstractmethod
    def add(self,user:UserRegister)->UserRegister:
        pass


    @abstractmethod
    def get_by_name(self,username:str)->UserRegister | None:
        pass


    @abstractmethod
    def get_by_email(self,email:str)->UserRegister|None:
        pass