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
wishlist_controller = Router(tags=['Wishlists'])


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


@wishlist_controller.get('all', auth=AuthBearer(), response={
    200: List[WishListOut],
    404: MessageOut
})
def get_wishlists(request):
    user = request.auth
    wishlist_qs = user.wishlists.all()
    if wishlist_qs:
        return response(status.HTTP_200_OK, wishlist_qs)
    return 404, {'message': 'no wishlists found'}


# add to wishlist
@wishlist_controller.post('add', auth=AuthBearer(), response={
    200: WishListOut,
    404: MessageOut
})
def add_to_wishlist(request, product_id: UUID4):
    user = request.auth
    product = Product.objects.get(id=product_id)
    if product:
        wishlist = user.wishlists.create(product=product)
        return response(status.HTTP_200_OK, wishlist)

    return 404, {'message': 'product not found'}


# remove from wishlist
@wishlist_controller.delete('remove', auth=AuthBearer(), response={
    202: MessageOut,
    404: MessageOut
})
def remove_from_wishlist(request, product_id: UUID4):
    user = request.auth
    product = Product.objects.get(id=product_id)
    if product:
        wishlist = user.wishlists.filter(product=product).delete()
        return response(status.HTTP_202_ACCEPTED, {'message': 'product removed from wishlist'})

    return 404, {'message': 'product not found'}