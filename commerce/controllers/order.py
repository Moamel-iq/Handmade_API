from django.contrib.auth import get_user_model
from ninja import Router

from Handmade.utils import status
from Handmade.utils.permissions import AuthBearer
from Handmade.utils.schemas import MessageOut
from Handmade.utils.utils import response
from commerce.models import Order, OrderStatus, Item
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


@order_controller.delete('/{order_id}', auth=AuthBearer(), response={
    200: MessageOut,
    404: MessageOut
})
def delete_order(request, order_id: int):
    order = Order.objects.filter(id=order_id, user=request.auth)
    if not order:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'No order found'})
    order.delete()
    return response(status.HTTP_200_OK, {'message': 'Order deleted successfully'})


@order_controller.post('/{order_id}/checkout', auth=AuthBearer(), response={
    200: MessageOut,
    404: MessageOut
})
def checkout_order(request, order_id: str):
    order = Order.objects.filter(id=order_id, user=request.auth)
    if not order:
        return response(status.HTTP_404_NOT_FOUND, {'message': 'No order found'})
    order.update(ordered=True)
    return response(status.HTTP_200_OK, {'message': 'Order checked out successfully'})

