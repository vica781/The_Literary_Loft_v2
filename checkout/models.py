from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import Sum
from django.conf import settings
from books.models import Book
from typing import Self, Optional
from django.db.models.signals import post_save
from django.dispatch import receiver

# ORDER INFORMATION


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name='orders'
        )
    guest_email = models.EmailField(max_length=254, null=True, blank=True)
    order_number = models.CharField(max_length=36, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=False,
        default=0
        )
    order_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
        )
    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        default=0
        )

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def update_total(self: Self) -> None:
        """Update order totals."""
        self.order_total = self.items.aggregate(
            Sum('item_total'))['item_total__sum'] or 0

        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_COST / 100)
        else:
            self.delivery_cost = 0

        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def __str__(self):
        return self.order_number


# ORDER ITEM INFORMATION
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        null=False,
        blank=False,
        related_name='items',
        on_delete=models.CASCADE
        )
    book = models.ForeignKey(
        Book,
        null=False,
        blank=False,
        on_delete=models.CASCADE
        )
    quantity = models.PositiveIntegerField(
        null=False,
        blank=False,
        default=0
        )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        editable=False
        )
    item_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
        default=0,
        editable=False
        )

    def save(self, *args, **kwargs):
        self.item_total = self.book.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantity} of {self.book.title}'


# USER PROFILE INFORMATION
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
        )
    default_full_name = models.CharField(
        max_length=50,
        null=True,
        blank=True
        )
    default_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
        )
    default_country = models.CharField(
        max_length=40,
        null=True,
        blank=True
        )
    default_postcode = models.CharField(
        max_length=20,
        null=True,
        blank=True
        )
    default_town_or_city = models.CharField(
        max_length=40,
        null=True,
        blank=True
        )
    default_street_address1 = models.CharField(
        max_length=80,
        null=True,
        blank=True
        )
    default_street_address2 = models.CharField(
        max_length=80,
        null=True,
        blank=True
        )
    default_county = models.CharField(
        max_length=80,
        null=True,
        blank=True
        )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    if hasattr(instance, 'profile'):
        instance.profile.save()
