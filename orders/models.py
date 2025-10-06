from typing import Iterable
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from decimal import Decimal

from store.models import Product


User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='orders'
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    status = models.CharField(
        max_length=40,
        choices=[
            ('pen', 'Pending'),
            ('ship', 'Shipped'),
            ('done', 'Done'),
        ],
        default='pen'
    )
    notes = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return f'Order: {self.pk}, by {self.user}.\nCurrent status: {self.status}'

    @property
    def total(self):
        return sum(Decimal(item.price) * item.quantity for item in self.items.all())

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at', 'user']


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    product_name_snapshot = models.CharField(
        max_length=255,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.product} in {self.order}'

    def save(self, *args, **kwargs) -> None:
        if self.product and not self.product_name_snapshot:
            self.product_name_snapshot = self.product.name
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['-added_at']
        unique_together = ('order', 'product',)
