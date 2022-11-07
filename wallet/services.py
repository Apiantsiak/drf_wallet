from random import choice, randint, shuffle
from string import ascii_uppercase

from django.core.exceptions import ValidationError

from .models import Wallets


def create_uid_wallet():
    up_letters_ls = list(ascii_uppercase)
    shuffle(up_letters_ls)
    gen_numbers = ("".join(str(randint(1, 9)) for _ in range(2)) for _ in range(2))
    gen_letters = ("".join(choice(up_letters_ls) for _ in range(2)) for _ in range(2))
    return (
        f"{next(gen_letters)}{next(gen_numbers)}{next(gen_letters)}{next(gen_numbers)}"
    )


def create_wallet_data(request):
    data = {}
    currency_balance = {
        "RUB": 100,
        "USD": 3,
        "EUR": 3,
    }
    data["currency"] = request.data["currency"]
    data["card_type"] = request.data["card_type"]
    data["balance"] = currency_balance[request.data["currency"]]
    data["wallet_name"] = create_uid_wallet()
    return data


def check_wallets_quantity(user):
    user_wallet_scope = Wallets.objects.filter(user=user).count()
    if user_wallet_scope >= 5:
        raise ValidationError("You can create only 5 wallets")
