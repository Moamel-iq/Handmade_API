from ninja import Schema

from pydantic import EmailStr, Field


class MessageOut(Schema):
    message: str


class AccountCreate(Schema):
    email: EmailStr = None
    password: str = None
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    address: str = None


class AccountSignupIn(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)
    phone_number: int


class AccountSignupOut(Schema):
    account: AccountCreate
    token: str


class AccountLoginData(Schema):
    email: EmailStr
    password: str


class ChangePassword(Schema):
    old_password: str
    new_password: str
    confirm_password: str
