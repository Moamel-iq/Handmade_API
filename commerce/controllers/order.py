from django.contrib.auth import get_user_model
from ninja import Router

from Handmade.utils import status
from Handmade.utils.permissions import AuthBearer
from Handmade.utils.schemas import MessageOut
from Handmade.utils.utils import response
from commerce.models import Order, OrderStatus, Item, Address
from commerce.schemas import *

User = get_user_model()

order_controller = Router(tags=['Orders'])


@order_controller.get('', auth=AuthBearer(), response={
    200: List[OrderOut],
    404: MessageOut
})
def all_orders(request, ordered: bool = False):
    order_qs = Order.objects.order_by('pk').filter(user=request.auth)
    if not ordered:
        order_qs = order_qs.filter(ordered=ordered)
    if not order_qs:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'No orders found'})
    return 200, order_qs


@order_controller.post('', auth=AuthBearer(), response={
    200: MessageOut,
    401: MessageOut
})
def create_update(request, items_in: OrderIn):
    items = Item.objects.filter(id__in=items_in.items)

    existing_order = Order.objects.filter(user=request.auth, ordered=False)

    if existing_order.exists():
        order_ = existing_order.first()
        for i in items:
            i.ordered = True
            i.save()
        order_.items.add(*items)
        order_.save()
        return response(status.HTTP_200_OK, {"message": "order updated successfully"})
    else:
        for i in items:
            i.ordered = True
            i.save()
        default_status = OrderStatus.objects.get(title="NEW")
        order_ = Order.objects.create(
            user=request.auth,
            status=default_status,
            ordered=False,

        )
        order_.items.add(*items)
        order_.save()
        return response(status.HTTP_200_OK, {"message": "order created successfully"})

#
@order_controller.post('/checkout', auth=AuthBearer(), response={
    200: MessageOut,
    404: MessageOut,
    400: MessageOut
})
def checkout(request):
    try:
        checkout_order = Order.objects.get(ordered=False, user=request.auth)
    except Order.DoesNotExist:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'Order not found'})
    address = Address.objects.get(user=request.auth)
    checkout_order.address = address
    if not checkout_order.address:
        return response(status.HTTP_400_BAD_REQUEST, {'message': 'order should have an address assigned'})

    checkout_order.shipping = checkout_order.order_shipment
    checkout_order.total = checkout_order.order_total
    for i in checkout_order.items.all():
        if i.product.qty < i.item_qty:
            return response(status.HTTP_404_NOT_FOUND, {
                'message': f'item {i.product.name} is out of stock!'
            })
        i.product.qty -= i.item_qty
        i.product.save()
    checkout_order.ordered = True
    checkout_order.save()
    return response(status.HTTP_200_OK, {'message': 'checkout successful'})


# @order_controller.post('/{pk}/update_address', auth=AuthBearer(), response={200: MessageOut, 404: MessageOut})
# def update_address(request, order_pk: UUID4, address_pk: UUID4):
#     try:
#         address = Address.objects.get(pk=address_pk, user=request.auth)
#     except Address.DoesNotExist:
#         return response(status.HTTP_404_NOT_FOUND, {'message': 'Address does not exist'})
#
#     try:
#         order_qs = Order.objects.get(pk=order_pk, user=request.auth)
#     except Order.DoesNotExist:
#         return response(status.HTTP_404_NOT_FOUND, {'message': 'Order does not exist'})
#
#     order_qs.address = address
#     order_qs.save()
#
#     return response(status.HTTP_200_OK, {'message': 'address updated successfully'})
