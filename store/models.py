from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

import uuid


User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True
        )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        amount_of_products = self.products.count()  # type: ignore
        return f'{self.name} includes {amount_of_products} products'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


#  Maybe it will be abstarct/base product model
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=120,
        blank=False,
        null=False,
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True
    )
    product_code = models.IntegerField(
        verbose_name='product code',
        blank=True,
        null=True,
    )
    # Add markdown support to admin site
    # or other way change default text widget
    description = models.TextField(
        blank=True,
        null=True
    )
    # I would like to remove details
    # and create custom class which extend base model by category
    details = models.TextField()
    in_stock = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
        )

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'{self.name} in stock: {self.in_stock}'

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']


class ProductImage(models.Model):
    image = models.ImageField(
        upload_to='products/images/'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self) -> str:
        return f'This image related to {self.product.name}'

    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'


class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
        )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        null=False,
        blank=False,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    content = models.CharField(
        max_length=200,
        blank=True,
        null=True
        )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'product')


class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )

    def __str__(self) -> str:
        return f'This wishlist owned by {self.user}'


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.product.name} in wishlist of {self.wishlist.user}'

    class Meta:
        ordering = ['-added_at']
