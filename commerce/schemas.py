from typing import List
from ninja import Schema
from pydantic import UUID4
from account.schemas import AccountData


class Profile(Schema):
    id: UUID4
    account: AccountData
    first_name: str
    last_name: str
    phone_number: str
    address: str
    city: str
    is_verified: bool


class Category(Schema):
    id: UUID4
    name: str
    description: str
    image: str
    is_active: bool
    children: List['Category'] = None


Category.update_forward_refs()


class ImageCreate(Schema):
    product_id: UUID4
    is_default_image: bool
    image: str


class ProductImageOut(Schema, ImageCreate):
    id: UUID4
    image: str


class Product(Schema):
    id: UUID4
    name: str
    price: int
    discounted_price: int
    description: str
    is_default: bool
    is_active: bool
    images: List[ProductImageOut] = None
    weight: float
    width: float
    height: float
    length: float
    qty: int
    category: Category


class Order(Schema):
    id: UUID4
    order_id: str
    total: float
    status: str
    products: list[Product]
    created_at: str
    updated_at: str


class CommentData(Schema):
    id: UUID4
    product_id: UUID4
    user_id: UUID4
    comment: str
    created_at: str
    updated_at: str
    user: AccountData
