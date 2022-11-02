from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase


CREATE_USER_URL = '/api/auth/users/'
TOKEN_URL = '/api/auth/token/login/'
ME_URL = f'{CREATE_USER_URL}me/'

USER = get_user_model()

PAYLOAD = {
    'test_user_1': {
        "username": "test_1",
        "email": "test_1@test.com",
        "password": "user_1_pass",
    },
    'test_user_2': {
        "username": "test_2",
        "email": "test_2@test.com",
        "password": "user_2_pass"
    }
}


class UsersTests(APITestCase):

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""

        response = self.client.post(CREATE_USER_URL, PAYLOAD['test_user_1'])
        user = get_user_model().objects.get(email=PAYLOAD['test_user_1']['email'])
        self.assertTrue(user.check_password(PAYLOAD['test_user_1']['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating user that already exists"""

        USER.objects.create_user(**PAYLOAD['test_user_1'])
        response = self.client.post(CREATE_USER_URL, PAYLOAD['test_user_1'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""

        PAYLOAD['test_user_1']['password'] = 'pass'
        response = self.client.post(CREATE_USER_URL, PAYLOAD['test_user_1'])
        user_exists = USER.objects.filter(email=PAYLOAD['test_user_1']['email']).exists()
        self.assertFalse(user_exists)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test that a token created for user"""

        response = self.client.post(CREATE_USER_URL, PAYLOAD['test_user_1'])
        user_data = {
            'username': PAYLOAD['test_user_1']['username'],
            'password': PAYLOAD['test_user_1']['password']
        }
        token_response = self.client.post(TOKEN_URL, user_data)
        self.assertIn('auth_token', token_response.data)
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_cred(self):
        """Test that token is not created when invalid credential are given"""

        response = self.client.post(CREATE_USER_URL, PAYLOAD['test_user_1'])
        invalid_user_data = {
            'username': PAYLOAD['test_user_2']['username'],
            'password': PAYLOAD['test_user_2']['password']
        }
        token_response = self.client.post(TOKEN_URL, invalid_user_data)
        self.assertNotIn('auth_token', token_response.data)
        self.assertEqual(token_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""

        user_exists = USER.objects.filter(email=PAYLOAD['test_user_1']['email']).exists()
        response = self.client.post(TOKEN_URL, PAYLOAD['test_user_1'])
        self.assertFalse(user_exists)
        self.assertNotIn('auth_token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that username and password are required"""

        response = self.client.post(TOKEN_URL, {'username': '', 'password': ''})
        self.assertNotIn('auth_token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
