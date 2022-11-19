from random import choice as ch
from typing import Dict, List, Union

from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.test import tag
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase
from wallet.models import CardType, Currency, Wallets


def get_wallet_data(
    scope: int = 1, currency=Currency.USD, card_type=CardType.VISA
) -> Union[Dict[str, str], List[Dict[str, str]]]:
    if scope > 1:
        data = [
            {"currency": ch(Currency.values), "card_type": ch(CardType.values)}
            for _ in range(scope)
        ]
        return data
    else:
        return {"currency": currency, "card_type": card_type}


class WalletsTests(APITestCase):
    TEST_URL = "/api/wallets/"

    def setUp(self):
        self.factory = APIRequestFactory()
        self.wallet_query_set: Wallets = Wallets.objects.all()
        self.user: CustomUser = get_user_model().objects.create_user(
            username="test_name", email="test_mail@test.com", password="secret_pass"
        )
        self.client.force_authenticate(user=self.user)

    @tag("create_wallet")
    def test_create_wallet(self):
        """Test creating wallet"""

        data = get_wallet_data()
        response = self.client.post(self.TEST_URL, data)
        wallet = self.wallet_query_set.filter(
            user=self.user, wallet_name=response.data["wallet_name"]
        ).exists()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(wallet)

    @tag("create_many_diff_wallets")
    def test_create_wallet_different_currency_card_type(self):
        """Test creating wallets with different currencies and card types"""

        wallets_data = get_wallet_data(3)
        for data in wallets_data:
            response = self.client.post(self.TEST_URL, data)
            wallet = self.wallet_query_set.filter(
                user=self.user, wallet_name=response.data["wallet_name"]
            ).exists()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(wallet)

    @tag("get_wallets_info")
    def test_get_wallets_info(self):
        """Test get user's wallets list"""

        wallets_data = get_wallet_data(5)
        response_data = []
        for data in wallets_data:
            response = self.client.post(self.TEST_URL, data)
            response_data.append(response.data)
        response = self.client.get(self.TEST_URL)
        self.assertEqual(response.data, response_data)

    @tag("detail_wallet_info")
    def test_get_wallet_by_wallet_name(self):
        """Test get wallet info by wallet name"""

        data = get_wallet_data()
        post_response = self.client.post(self.TEST_URL, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        wallet_name = post_response.data["wallet_name"]
        get_response = self.client.get(f"{self.TEST_URL}{wallet_name}/")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["wallet_name"], wallet_name)

    @tag("delete_wallet")
    def test_delete_wallet(self):
        """Test delete user's wallet"""

        data = get_wallet_data()
        post_response = self.client.post(self.TEST_URL, data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        wallet_exist = self.wallet_query_set.filter(
            wallet_name=post_response.data["wallet_name"]
        ).exists()
        self.assertTrue(wallet_exist)
        wallet = self.wallet_query_set.get(
            wallet_name=post_response.data["wallet_name"]
        )
        delete_response = self.client.delete(
            f"{self.TEST_URL}{wallet.wallet_name}/", data
        )
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        wallet_dont_exist = self.wallet_query_set.filter(
            wallet_name=wallet.wallet_name
        ).exists()
        self.assertFalse(wallet_dont_exist)

    @tag("wallets_limit")
    def test_wallet_limit(self):
        """Test that the user is able to create only 5 wallets"""

        wallets_data = get_wallet_data(5)
        for data in wallets_data:
            response = self.client.post(self.TEST_URL, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        counter = self.wallet_query_set.filter(user=self.user).count()
        self.assertEqual(counter, 5)
        response = self.client.post(self.TEST_URL, wallets_data[0])
        self.assertEqual(response.data, {"error": "You can create only 5 wallets"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
