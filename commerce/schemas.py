from typing import List
from ninja import Schema, ModelSchema
from ninja.orm import create_schema
from pydantic import UUID4, UUID5
from account.schemas import AccountOut
from commerce.models import  OrderStatus


class Profile(Schema):
    id: UUID4
    account: AccountOut
    first_name: str
    last_name: str
    phone_number: str
    address: str
    city: str
    is_verified: bool


class CategoryData(Schema):
    id: UUID4
    name: str
    description: str = None
    image: str = None
    is_active: bool
    children: List['CategoryData'] = None


CategoryData.update_forward_refs()


class ImageCreate(Schema):
    product_id: UUID4
    is_default_image: bool


class ProductImageOut(Schema):
    id: UUID4
    image: str


class ProductOut(Schema):
    id: UUID4
    name: str
    description: str = None
    in_stock: bool = None
    qty: int
    price: float
    new_price: float = None
    category: CategoryData = None
    is_featured: bool = None
    is_active: bool = None
    images: List[ProductImageOut] = None


class ProductDataOut(Schema):
    total_count: int = None
    per_page: int = None
    from_record: int = None
    to_record: int = None
    previous_page: int = None
    next_page: int = None
    current_page: int = None
    page_count: int = None
    data: List[ProductOut]


class ProductCreate(Schema):
    name: str
    description: str
    in_stock: bool
    qty: int
    category_id: UUID4
    is_featured: bool
    is_active: bool
    images: List[ImageCreate]


class ItemOut(Schema):
    id: UUID4
    product: ProductOut
    item_qty: int
    ordered: bool


class ItemIn(Schema):
    product_id: UUID4
    item_qty: int = None


OrderStatusDataOut = create_schema(OrderStatus, exclude=['id', 'created', 'updated'])


class OrderOut(Schema):
    id: UUID4
    user: AccountOut
    order_total: float
    status: OrderStatusDataOut
    items: List[ItemOut]


class OrderIn(Schema):
    items: List[UUID4]


class WishListOut(Schema):
    id: UUID4
    product: ProductOut


class WishListIn(Schema):
    product_id: UUID4
