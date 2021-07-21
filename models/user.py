from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    is_admin: bool=False
    
    

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Mehdi Nurullah",
                "email": "mehdi@laroza.dev",
                "password": "password123",
            }
        }

class UserPassModel(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    
    

    class Config:
        schema_extra = {
            "example": {
                "email": "mehdi@laroza.dev",
                "password": "password123",
            }
        }


class UpdateUserModel(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]
    class Config:
        schema_extra = {
            "example": {
                "fullname": "Mehdi Nurullah",
                "email": "mehdi@laroza.dev",
                "password": "password456",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [
            data
        ],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {
        "error": error,
        "code": code,
        "message": message
    }
