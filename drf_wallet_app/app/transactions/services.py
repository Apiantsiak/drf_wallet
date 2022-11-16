from decimal import Decimal, getcontext
from typing import NoReturn, Union

from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import transaction
from wallet.models import Wallets

from .models import Status, Transaction


def make_transaction(
    sender: Wallets, receiver: Wallets, transaction_amount: Union[str, int]
) -> NoReturn:
    getcontext().prec = 2
    transaction_amount = Decimal(transaction_amount)
    tax = 0
    if sender.user != receiver.user:
        tax = transaction_amount * Decimal(0.10)
        transaction_amount += tax
    try:
        if sender.balance < transaction_amount:
            raise ValueError("Not enough money")
        if sender.currency != receiver.currency:
            raise ValueError("Wallet currency don't match")
        with transaction.atomic():
            from_balance = sender.balance - transaction_amount
            sender.balance = from_balance
            sender.save()

            to_balance = receiver.balance + transaction_amount
            receiver.balance = to_balance
            receiver.save()

            valid_transaction = Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                transaction_amount=transaction_amount,
                commission=tax,
                status=Status.PAID,
            )
    except ValueError as err:
        invalid_transaction = Transaction.objects.create(
            sender=sender,
            receiver=receiver,
            transaction_amount=transaction_amount,
            commission=tax,
        )
        raise ValidationError(str(err))


def filter_user_wallet(user: CustomUser, sender: Wallets) -> Wallets:
    try:
        wallet = Wallets.objects.filter(user=user).get(wallet_name=sender)
    except Wallets.DoesNotExist:
        raise ValidationError("Wallet doesn't exist")

    return wallet


def check_receiver_wallet_exists(receiver: Wallets) -> Wallets:
    try:
        wallet = Wallets.objects.get(wallet_name=receiver)
    except Wallets.DoesNotExist:
        raise ValidationError("Wallet doesn't exist")

    return wallet
