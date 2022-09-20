from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import UUID4
from typing import List

from Handmade.utils import status
from Handmade.utils.schemas import MessageOut
from Handmade.utils.utils import response
from commerce.models import Product
from commerce.schemas import ProductDataOut, ProductOut

User = get_user_model()

product_controller = Router(tags=['Products'])


@product_controller.get('/all', auth=None, response={
    200: ProductDataOut,
    404: MessageOut
})
def all_products(request, category=None, search=None, per_page: int = 12, page: int = 1):
    if category:
        products = Product.objects.filter(category__name=category)
    elif search:
        products = Product.objects.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    else:
        products = Product.objects.all()
    if products:
        return response(status.HTTP_200_OK, products, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No products found'}


@product_controller.get('/{pk}', auth=None, response={
    200: ProductOut,
    404: MessageOut
})
def retrieve_product(request, pk: UUID4):
    product = Product.objects.get(id=pk)
    if product:
        return 200, product
    return 404, {'message': 'No product found'}


