from django.contrib import admin

from commerce.models import *

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderStatus)
admin.site.register(City)
admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(Images)
admin.site.register(Comment)