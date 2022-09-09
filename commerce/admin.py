from django.contrib import admin
from commerce.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'category', 'label', 'image')
    list_filter = ('name', 'price', 'description', 'category', 'label', 'image')
    search_fields = ('name', 'price', 'description', 'category', 'label', 'image')
    ordering = ('name', 'price', 'description', 'category', 'label', 'image')

    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'description', 'category', 'label', 'image')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image')
    list_filter = ('name', 'description', 'image')
    search_fields = ('name', 'description', 'image')
    ordering = ('name', 'description', 'image')

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'image')
        }),
    )


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user', 'product', 'quantity', 'ordered', 'created', 'updated')
#     list_filter = ('user', 'product', 'quantity', 'ordered', 'created', 'updated')
#     search_fields = ('user', 'product', 'quantity', 'ordered', 'created', 'updated')
#     ordering = ('user', 'product', 'quantity', 'ordered', 'created', 'updated')
#
#     fieldsets = (
#         (None, {
#             'fields': ('user', 'product', 'quantity', 'ordered', 'created', 'updated')
#         }),
#     )

