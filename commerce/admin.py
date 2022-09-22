from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from nested_inline.admin import NestedModelAdmin

from account.models import Profile
from commerce.models import *


# admin.site.register(OrderStatus)


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
    search_fields = ['name']
    list_per_page = 20


class ItemInline(admin.TabularInline):
    model = Order.items.through
    inlines = []
    extra = 1


@admin.register(Order)
class OrderAdmin(NestedModelAdmin):
    inlines = [ItemInline]
    list_display = ['user', 'status', 'order_total']
    list_filter = ['status']
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ['indented_title', 'parent', 'name', 'image', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']
    list_per_page = 20


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
    list_per_page = 20


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    list_filter = ['address']
    list_per_page = 20


@admin.register(ColorProduct)
class ColorProductAdmin(admin.ModelAdmin):
    list_display = ['color', 'product']
    list_filter = ['color']
    list_per_page = 20


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['user', 'product', 'comment']
#     list_filter = ['product']
#     list_per_page = 20


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    list_filter = ['product']
    list_per_page = 20


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'item_qty']
    list_filter = ['product']
    list_per_page = 20


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_default']
    list_filter = ['is_default', 'title']
    list_per_page = 20


# @admin.register(Address)
# class AddressAdmin(admin.ModelAdmin):
#     list_display = ['user', 'address']
#     list_per_page = 20




