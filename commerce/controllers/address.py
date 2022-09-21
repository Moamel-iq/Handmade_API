from typing import List

from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import UUID4

from Handmade.utils.permissions import AuthBearer
from commerce.models import Address, City
from commerce.schemas import AddressOut, AddressCreate, CityOut
from Handmade.utils.schemas import MessageOut

address_controller = Router(tags=['Addresses'])


@address_controller.get('', response={
    200: List[AddressOut],
    404: MessageOut
})
def get_addresses(request):
    address_qs = Address.objects.all()
    if address_qs:
        return 200, address_qs
    return 404, {'message': 'No addresses found'}


