from ninja import Schema
from pydantic import UUID4


class TokenAuth(Schema):
    id: str
    exp: str
    sub: str
