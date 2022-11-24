from pydantic import BaseModel, ValidationError, validator
from typing import Optional

class SignupModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                'username':'Nishant',
                'email': 'nishant55@gmail.com',
                'password': 'password',
                'is_staff':False,
                'is_active':True

            }

        }
class Settings(BaseModel):
    authjwt_secret_key:str='86a2edbed7857f09757da135af29131a134fd6905fb4fea480bdbdb5c7aed6ba'

class LoginModel(BaseModel):
    username:str
    password:str

class OrderModel(BaseModel):
    id : Optional[int]
    quantity : int
    order_status : Optional[str]='PENDING'
    pizza_size : Optional[str]='SMALL'
    userid:Optional[str]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                'quantity':2,
                'pizza_size':'LARGE'
            }
        }
class OrderStatus(BaseModel):
    order_status:Optional[str]="PENDING"
    class config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status" : "PENDING"
            }
        }


