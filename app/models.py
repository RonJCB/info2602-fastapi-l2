from sqlmodel import Field, SQLModel
from typing import Optional
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

class User(SQLModel, table=True):
    id: Optional[int] =  Field(default=None, primary_key=True)
    username:str = Field(index=True, unique=True)
    email:str = Field(index=True, unique=True)
    password:str
#added 3 methods to the user class 
#first one makes a intances of the class
#second one 
#third one prints the instance to the console
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = password_hash.hash(password)

    def __str__(self) ->str:
        return f"(User id = {self.id}, username = {self.username}, email = {self.email})"