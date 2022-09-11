from django.contrib import admin
from nested_inline.admin import NestedModelAdmin
from commerce.models import *
from easy_select2 import select2_modelform

# admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Item)
admin.site.register(OrderStatus)
# admin.site.register(City)
# admin.site.register(Address)
admin.site.register(Profile)
admin.site.register(Images)
admin.site.register(Comment)
admin.site.register(ColorProduct)
admin.site.register(Wishlist)


class ProductImage(admin.TabularInline):
    model = Images
    inlines = []
    extra = 9


class ProductColor(admin.TabularInline):
    model = ColorProduct
    inlines = []
    extra = 1


@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    inlines = [ProductColor, ProductImage]

    list_display = ['name', 'price', 'category', 'is_active']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'price', 'category']
    list_per_page = 20
