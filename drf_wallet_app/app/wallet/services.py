from random import choice, randint, shuffle
from string import ascii_uppercase
from typing import Dict

from accounts.models import CustomUser
from django.core.exceptions import ValidationError

from .models import Currency, Wallets


def create_wallet_uid() -> str:
    up_letters_ls = list(ascii_uppercase)
    shuffle(up_letters_ls)
    gen_numbers = ("".join(str(randint(1, 9)) for _ in range(2)) for _ in range(2))
    gen_letters = ("".join(choice(up_letters_ls) for _ in range(2)) for _ in range(2))
    return (
        f"{next(gen_letters)}{next(gen_numbers)}{next(gen_letters)}{next(gen_numbers)}"
    )


def create_wallet_data(request) -> Dict[str, str]:
    data = {}
    if request.data:
        currency_balance = {
            Currency.RUB: 100,
            Currency.USD: 3,
            Currency.EUR: 3,
        }
        data["currency"] = request.data.get("currency", None)
        data["card_type"] = request.data.get("card_type", None)
        data["balance"] = currency_balance[request.data["currency"]]
        data["wallet_name"] = create_wallet_uid()
    return data


def check_wallets_quantity(user: CustomUser):
    user_wallet_scope = Wallets.objects.filter(user=user).count()
    if user_wallet_scope == 5:
        raise ValidationError("You can create only 5 wallets")
