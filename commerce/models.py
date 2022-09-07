
from django.db import models
from ckeditor.fields import RichTextField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
import uuid
from tkinter import Image
from django.contrib.auth import get_user_model

User = get_user_model()


class Entity(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

# class Customer(models.Model):
#     user=models.OneToOneField(User,on_delete=models.CASCADE)
#     profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
#     address = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=20,null=False)
#     @property
#     def get_name(self):
#         return self.user.first_name+" "+self.user.last_name
#     @property
#     def get_id(self):
#         return self.user.id
#     def __str__(self):
#         return self.user.first_name


class Product(Entity):
    name = models.CharField('name', max_length=255)
    description = RichTextField('description', null=True, blank=True)
    weight = models.FloatField('weight', null=True, blank=True)
    width = models.FloatField('width', null=True, blank=True)
    height = models.FloatField('height', null=True, blank=True)
    length = models.FloatField('length', null=True, blank=True)
    qty = models.DecimalField('qty', max_digits=10, decimal_places=2)
    cost = models.DecimalField('cost', max_digits=10, decimal_places=2)
    price = models.DecimalField('price', max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField('discounted price', max_digits=10, decimal_places=2)
    category = models.ForeignKey('commerce.Category', verbose_name='category', related_name='products',
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    is_featured = models.BooleanField('is featured')
    is_active = models.BooleanField('is active')
    # is_discounted = models.BooleanField('is discounted')
    # is_new = models.BooleanField('is new')
    # is_best_seller = models.BooleanField('is best seller')
    # is_on_sale = models.BooleanField('is on sale')
    # is_top_rated = models.BooleanField('is top rated')
    # is_trending = models.BooleanField('is trending')
    # is_hot_deal = models.BooleanField('is hot deal')
    # is_out_of_stock = models.BooleanField('is out of stock')
    # is_free_shipping = models.BooleanField('is free shipping')
    # is_in_stock = models.BooleanField('is in stock')
    label = models.ForeignKey('commerce.Label', verbose_name='label', related_name='products', null=True, blank=True,
                              on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(MPTTModel, Entity):
    parent = TreeForeignKey('self', verbose_name='parent', related_name='children',
                            null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField('name', max_length=255)
    description = models.TextField('description')
    image = models.ImageField('image', upload_to='category/')
    is_active = models.BooleanField('is active')

    created = models.DateField(editable=False, auto_now_add=True)
    updated = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        verbose_name_plural = 'categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        if self.parent:
            return f'-   {self.name}'
        return f'{self.name}'


class Order(Entity):
    user = models.ForeignKey(User, verbose_name='user', related_name='orders', null=True, blank=True,
                             on_delete=models.CASCADE)
    address = models.ForeignKey('commerce.Address', verbose_name='address', null=True, blank=True,
                                on_delete=models.CASCADE)
    total = models.DecimalField('total', blank=True, null=True, max_digits=1000, decimal_places=0)
    status = models.ForeignKey('commerce.OrderStatus', verbose_name='status', related_name='orders',
                               on_delete=models.CASCADE)
    note = models.CharField('note', null=True, blank=True, max_length=255)
    ref_code = models.CharField('ref code', max_length=255)
    ordered = models.BooleanField('ordered')
    items = models.ManyToManyField('commerce.Item', verbose_name='items', related_name='order')

    def __str__(self):
        return f'{self.user.first_name} + {self.total}'

    @property
    def order_total(self):
        order_total = sum(
            i.product.price_discounted * i.item_qty for i in self.items.all()
        )

        return order_total


class Item(Entity):
    """
    Product can live alone in the system, while
    Item can only live within an order
    """
    user = models.ForeignKey(User, verbose_name='user', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('commerce.Product', verbose_name='product',
                                on_delete=models.CASCADE)
    item_qty = models.IntegerField('item_qty')
    ordered = models.BooleanField('ordered')

    def __str__(self):
        return f'self.product.name'


class OrderStatus(Entity):
    NEW = 'NEW'  # Order with reference created, items are in the basket.
    PROCESSING = 'PROCESSING'  # Payment confirmed, processing order.
    SHIPPED = 'SHIPPED'  # Shipped to customer.
    COMPLETED = 'COMPLETED'  # Completed and received by customer.
    REFUNDED = 'REFUNDED'  # Fully refunded by seller.

    title = models.CharField('title', max_length=255, choices=[
        (NEW, NEW),
        (PROCESSING, PROCESSING),
        (SHIPPED, SHIPPED),
        (COMPLETED, COMPLETED),
        (REFUNDED, REFUNDED),
    ])
    is_default = models.BooleanField('is default')

    def __str__(self):
        return self.title


class ProductImage(Entity):
    image = models.ImageField('image', upload_to='product/')
    is_default_image = models.BooleanField('is default image')
    product = models.ForeignKey('commerce.Product', verbose_name='product', related_name='images',
                                on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)
            # print(self.image.path)


class Label(Entity):
    name = models.CharField('name', max_length=255)

    class Meta:
        verbose_name = 'label'
        verbose_name_plural = 'labels'

    def __str__(self):
        return self.name


class City(Entity):
    name = models.CharField('city', max_length=255)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name


class Address(Entity):
    user = models.ForeignKey(User, verbose_name='user', related_name='address',
                             on_delete=models.CASCADE)
    address = models.CharField('address1', max_length=255)
    city = models.ForeignKey(City, related_name='addresses', on_delete=models.CASCADE)
    phone = models.CharField('phone', max_length=255)

    def __str__(self):
        return f'{self.user.first_name} - {self.address}  - {self.phone}'


class DeliveryMap(Entity):
    city = models.ForeignKey(City, related_name='delivery_map', on_delete=models.CASCADE)
    delivery_cost = models.IntegerField('delivery cost')

    def __str__(self):
        return f'{self.city.name} - {self.delivery_cost}'

# class Rating(Entity):
#     user = models.ForeignKey(User, verbose_name='user', related_name='ratings',
#                              on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, verbose_name='product', related_name='ratings',
#                                 on_delete=models.CASCADE)
#     rating = models.IntegerField('rating')
#
#     def __str__(self):
#         return f'{self.user.first_name} - {self.product.name} - {self.rating}'
#
#
# class Comment(Entity):
#     user = models.ForeignKey(User, verbose_name='user', related_name='comments',
#                              on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, verbose_name='product', related_name='comments',
#                                 on_delete=models.CASCADE)
#     comment = models.TextField('comment')
#
#     def __str__(self):
#         return f'{self.user.first_name} - {self.product.name} - {self.comment}'
#
#
# class Wishlist(Entity):
#     user = models.ForeignKey(User, verbose_name='user', related_name='wishlists',
#                              on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, verbose_name='product', related_name='wishlists',
#                                 on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.user.first_name} - {self.product.name}'
