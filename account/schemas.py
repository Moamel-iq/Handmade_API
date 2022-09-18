import datetime

from ninja import Schema
from pydantic import EmailStr, UUID4

from Handmade.utils.schemas import Token


class AccountOut(Schema):
    email: EmailStr
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    address: str = None
    date_joined: datetime.datetime
    is_verified: bool = None


class AccountSignupIn(Schema):
    first_name: str
    last_name: str
    email: EmailStr
    phone: int
    password1: str
    password2: str


class AccountSignupOut(Schema):
    profile: AccountOut
    token: Token


class AccountConfirmationIn(Schema):
    email: EmailStr
    verification_code: str


class AccountUpdateIn(Schema):
    first_name: str = None
    last_name: str = None
    email: str = None
    phone_number: str = None
    address: str = None


class AccountSigninOut(Schema):
    profile: AccountOut
    token: Token


class AccountSigninIn(Schema):
    email: EmailStr
    password: str


class PasswordChangeIn(Schema):
    old_password: str
    new_password1: str
    new_password2: str


class Profile(Schema):
    id: UUID4
    account: AccountOut
    first_name: str
    last_name: str
    phone_number: str
    address: str
    city: str
    is_verified: bool
