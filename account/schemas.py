from ninja import Schema

from pydantic import EmailStr, Field


class AccountData(Schema):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str
    address: str
    is_verified: bool


class AccountSignupData(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)
    phone_number: int


class AccountLoginData(Schema):
    email: EmailStr
    password: str


class ChangePassword(Schema):
    old_password: str
    new_password: str
    confirm_password: str






