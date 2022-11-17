from typing import Dict, List, Union

from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from transactions.models import Status, Transaction
from wallet.models import CardType, Currency, Wallets
from wallet.services import create_wallet_uid


def create_user_wallet(
    user: CustomUser,
    currency: Currency = Currency.USD,
    card_type: CardType = CardType.VISA,
    balance: Union[int, float] = 10,
) -> Wallets:
    wallet = Wallets.objects.create(
        user=user,
        currency=currency,
        card_type=card_type,
        wallet_name=create_wallet_uid(),
        balance=balance,
    )
    return wallet


def create_transaction_data(
    sender: Wallets, receiver: Wallets, transaction_amount: Union[int, float]
) -> Dict[str, Union[str, int, float]]:
    data = {
        "sender": sender.wallet_name,
        "receiver": receiver.wallet_name,
        "transaction_amount": transaction_amount,
    }
    return data


class TransactionsTests(APITestCase):
    TEST_URL = "/api/wallets/transactions/"
    TAX_RATE = 0.10

    @classmethod
    def setUpTestData(cls):
        cls.sender: CustomUser = get_user_model().objects.create_user(
            username="sender_name", email="sender@test.com", password="secret_pass"
        )
        cls.receiver: CustomUser = get_user_model().objects.create_user(
            username="receiver_name", email="receiver@test.com", password="secret_pass"
        )
        # By default, user's wallets have USD currencies and VISA card types

        cls.sender_wallet = create_user_wallet(user=cls.sender)
        cls.receiver_wallet = create_user_wallet(user=cls.receiver)

    def setUp(self):
        self.transaction_query_set = Transaction.objects.all()
        self.client.force_authenticate(user=self.sender)

    def test_make_transaction_one_user(self):
        second_user_wallet = create_user_wallet(self.sender)
        transaction_amount = 5
        commission = 0
        data = create_transaction_data(
            self.sender_wallet, second_user_wallet, transaction_amount
        )
        post_response = self.client.post(self.TEST_URL, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        sender_balance = Wallets.objects.get(
            user=self.sender, wallet_name=self.sender_wallet.wallet_name
        ).balance
        receiver_balance = Wallets.objects.get(
            user=self.sender, wallet_name=second_user_wallet.wallet_name
        ).balance
        transaction = self.transaction_query_set.get(
            sender=self.sender_wallet.wallet_name
        )
        self.assertEqual(sender_balance, 5)
        self.assertEqual(receiver_balance, 15)
        self.assertEqual(transaction.status, Status.PAID)
        self.assertEqual(transaction.commission, commission)

    def test_make_transaction_diff_users(self):
        transaction_amount = 5
        commission = transaction_amount * self.TAX_RATE
        data = create_transaction_data(
            self.sender_wallet, self.receiver_wallet, transaction_amount
        )
        post_response = self.client.post(self.TEST_URL, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        sender_balance = Wallets.objects.get(
            user=self.sender, wallet_name=self.sender_wallet.wallet_name
        ).balance
        receiver_balance = Wallets.objects.get(
            user=self.receiver, wallet_name=self.receiver_wallet.wallet_name
        ).balance
        transaction = self.transaction_query_set.get(
            sender=self.sender_wallet.wallet_name
        )
        self.assertEqual(sender_balance, 4.50)
        self.assertEqual(receiver_balance, 15)
        self.assertEqual(transaction.status, Status.PAID)
        self.assertEqual(transaction.commission, commission)

    def test_get_user_transactions_list(self):
        data = create_transaction_data(
            self.sender_wallet, self.receiver_wallet, transaction_amount=2
        )
        for _ in range(3):
            post_response = self.client.post(self.TEST_URL, data)
            self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        get_response = self.client.get(self.TEST_URL)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        transactions_in_db = self.transaction_query_set.filter(
            sender=self.sender_wallet
        ).count()
        self.assertEqual(transactions_in_db, len(get_response.data))

    def test_get_transaction_by_id(self):
        data = create_transaction_data(
            self.sender_wallet, self.receiver_wallet, transaction_amount=5
        )
        post_response = self.client.post(self.TEST_URL, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        transactions_id = self.transaction_query_set.get(sender=self.sender_wallet).pk
        get_response = self.client.get(f"{self.TEST_URL}{transactions_id}/")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

    def test_get_transaction_where_sender_or_receiver(self):
        data = create_transaction_data(
            self.sender_wallet, self.receiver_wallet, transaction_amount=5
        )
        post_response = self.client.post(self.TEST_URL, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=self.receiver)
        data = create_transaction_data(
            self.receiver_wallet, self.sender_wallet, transaction_amount=5
        )
        post_response = self.client.post(self.TEST_URL, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=self.sender)
        get_response = self.client.get(
            f"{self.TEST_URL}{self.sender_wallet.wallet_name}/"
        )
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        print(get_response.data)

    def test_not_enough_money(self):
        second_user_wallet = create_user_wallet(self.sender, balance=0)
        data = create_transaction_data(
            second_user_wallet, self.sender_wallet, transaction_amount=1
        )
        post_response = self.client.post(self.TEST_URL, data)
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(post_response.data, {"error": "Not enough money"})

    def test_transaction_diff_currency(self):
        second_user_wallet = create_user_wallet(
            self.sender, currency=Currency.EUR, balance=10
        )
        data = create_transaction_data(
            second_user_wallet, self.sender_wallet, transaction_amount=5
        )
        post_response = self.client.post(self.TEST_URL, data)
        self.assertEqual(post_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            post_response.data, {"error": "Wallet's currencies don't match"}
        )
