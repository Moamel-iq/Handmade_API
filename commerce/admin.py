from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from nested_inline.admin import NestedModelAdmin
from commerce.models import *

admin.site.register(Item)
# admin.site.register(Category)
admin.site.register(OrderStatus)
admin.site.register(Profile)
admin.site.register(Images)
admin.site.register(Comment)
admin.site.register(ColorProduct)
admin.site.register(Wishlist)


class ProductImage(admin.TabularInline):
    model = Images
    inlines = []
    extra = 1


class ProductColor(admin.TabularInline):
    model = ColorProduct
    inlines = []
    extra = 1


@admin.register(Product)
class ProductAdmin(NestedModelAdmin):
    inlines = [ProductColor, ProductImage]

    list_display = ['name', 'price', 'category', 'is_active', 'qty']
    list_filter = ['is_active', 'category']
    search_fields = ['name', 'price', 'category']
    list_per_page = 20


class ItemInline(admin.TabularInline):
    model = Order.items.through
    inlines = []
    extra = 1


@admin.register(Order)
class OrderAdmin(NestedModelAdmin):
    inlines = [ItemInline]
    list_display = ['user', 'status', 'order_total']
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ['indented_title', 'parent', 'name',  'image', 'is_active']
    list_per_page = 20
