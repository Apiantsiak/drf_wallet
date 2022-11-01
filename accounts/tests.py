from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient, APITestCase
from rest_framework import status


CREATE_USER_URL = '/api/auth/users/'
TOKEN_URL = '/auth/token/login/'


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UsersTests(APITestCase):

    def test_create_valid_user_success(self):
        """test creating user with valid payload is successful"""
        payload = {
            "email": "test@test.com",
            "username": "test_us",
            "password": "test_pass"
        }
        response = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(email=payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)
