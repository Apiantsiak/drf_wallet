from django.db import models

from wallet.models import Wallets


class Transaction(models.Model):
    sender = models.ForeignKey(
        Wallets, on_delete=models.CASCADE, related_name="sender", to_field="wallet_name"
    )
    receiver = models.ForeignKey(
        Wallets,
        on_delete=models.CASCADE,
        related_name="receiver",
        to_field="wallet_name",
    )
    transaction_amount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    commission = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    status = models.CharField(max_length=6, default="FAILED")
    created_at = models.DateTimeField(auto_now_add=True)
