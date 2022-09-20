from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ninja import Router, File
from ninja.files import UploadedFile

from Handmade.utils import status
from Handmade.utils.permissions import AuthBearer
from Handmade.utils.schemas import MessageOut
from Handmade.utils.utils import response
from commerce.models import Category, Images, Product
from commerce.schemas import *

User = get_user_model()

category_controller = Router(tags=['Categories'])
product_image_controller = Router(tags=['Product images'])
item_controller = Router(tags=['Items'])

# @product_image_controller.post('edit/{pk}', auth=AuthBearer(), response={
#     201: MessageOut,
#     400: MessageOut
# })
# def update_image(request, pk: UUID4, image: ImageEdit, image_in: UploadedFile = File(...)):
#     get_object_or_404(Product, images__id=pk, user=request.auth)
#     image_data = image.dict()
#     Images.objects.filter(id=pk).update(image=f'product/{image_in}', **image_data)
#     return 201, {'message': 'image updated successfully'}
#
#
# @product_image_controller.post('', auth=AuthBearer(), response={
#     201: MessageOut,
#     400: MessageOut
# })
# def add_image(request, image: ImageCreate, image_in: UploadedFile = File(...)):
#     image_data = image.dict()
#     product_instance = image_data.pop('product_id')
#     product = get_object_or_404(Product, id=product_instance,)
#     Images.objects.create(image=f'product/{image_in}', **image_data, product_id=product_instance)
#     return 201, {'message': 'image added successfully'}


# @product_image_controller.delete('{pk}', auth=AuthBearer(), response={
#     202: MessageOut
# })
# def delete_image(request, pk: UUID4):
#     image_qs = get_object_or_404(Images, id=pk)
#     image_qs.delete()
#     return 202, {'message': 'image deleted successfully'}


@category_controller.get('all', response={
    200: List[CategoryData],
    404: MessageOut
})
def get_categories(request):
    category_qs = Category.objects.filter(is_active=True).filter(parent=None)
    if category_qs:
        return 200, category_qs
    return 404, {'message': 'no categories found'}


@category_controller.get('{pk}', response={
    200: List[CategoryData],
    404: MessageOut
})
def retrieve_category(request, pk: UUID4):
    category_qs = Category.objects.filter(is_active=True, id=pk).filter(parent=None)
    if category_qs:
        return 200, category_qs
    return 404, {'message': 'no categories found'}


@category_controller.get('{pk}/products', response={
    200: ProductDataOut,
    404: MessageOut
})
def category_products(request, pk: UUID4, per_page: int = 12, page: int = 1):
    if pk is None:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'No category specified'})
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Category does not exist'})
    products = (
        Product.objects.filter(category__in=category.get_descendants(include_self=True))
        .select_related('category')
    )

    return response(status.HTTP_200_OK, products, paginated=True, per_page=per_page, page=page)

#
# @item_controller.get('all', response={
#     200: ProductDataOut,
#     404: MessageOut
# })
# def get_items(request, per_page: int = 12, page: int = 1):
#     items_qs = Product.objects.filter(is_active=True)
#     if items_qs:
#         return response(status.HTTP_200_OK, items_qs, paginated=True, per_page=per_page, page=page)
#     return response(status.HTTP_404_NOT_FOUND, {'message': 'No items found'})
#
#
# @item_controller.get('{pk}', response={
#     200: ProductDataOut,
#     404: MessageOut
# })
# def retrieve_item(request, pk: UUID4):
#     item_qs = get_object_or_404(Product, id=pk)
#     if item_qs:
#         return 200, item_qs
#     return 404, {'message': 'No item found'}