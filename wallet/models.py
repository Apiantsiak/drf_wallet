from django.conf import settings
from django.db import models


class Wallets(models.Model):
    CURRENCY = (
        ("USD", "USD"),
        ("EUR", "EUR"),
        ("RUB", "RUB"),
    )
    TYPE = (
        ("visa", "visa"),
        ("mastercard", "mastercard"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True
    )
    wallet_name = models.CharField(max_length=8, unique=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY)
    card_type = models.CharField(max_length=10, choices=TYPE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
