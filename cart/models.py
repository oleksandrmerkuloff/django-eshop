from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

import uuid

from store.models import Product


User = get_user_model()


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
        )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self) -> str:
        return f'{self.user}\'s cart'

    @property
    def total(self):
        return sum(item.price * item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='item'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1)
        ],
        null=False
    )
    price = models.DecimalField(
        blank=True,
        max_digits=6,
        decimal_places=2
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs) -> None:
        self.price = self.product.price
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.product} in {self.cart}'

    class Meta:
        ordering = ['-added_at']
        unique_together = ('cart', 'product',)
