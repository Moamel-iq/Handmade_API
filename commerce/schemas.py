from ninja import Schema


# schema for commerce

class Product(Schema):
    name: str
    price: int
    description: str
    category: str
    label: str
    image: str
    is_default: bool

