from django.contrib import admin
from django.urls import path, include
from ninja import NinjaAPI
from account.controllers import auth_controller
from commerce.controllers.cart import cart_controller
from commerce.controllers.order import order_controller
from commerce.controllers.others import category_controller, product_image_controller, item_controller, wishlist_controller
from commerce.controllers.product import product_controller

# from commerce.controllers.address import address_controller

api = NinjaAPI()
api.add_router('/auth', auth_controller)
api.add_router('/products', product_controller)
api.add_router('/carts', cart_controller)
api.add_router('/orders', order_controller)
api.add_router('/categories', category_controller)
api.add_router('/product-images', product_image_controller)
api.add_router('/items', item_controller)
api.add_router('/wishlists', wishlist_controller)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

# urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
