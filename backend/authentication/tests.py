from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from authentication.models import User

class AuthenticationTests(TestCase):
    def setUp(self):        
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'name': 'Test',
            'last_name': 'User',
            'password': 'testpassword',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_login(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('refresh-token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], self.user_data['username'])

    def test_logout(self):
        login_response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.data.get('token', '')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        # Intento de logout
        logout_response = self.client.post(self.logout_url, format='json')
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertIn('Sesión cerrada correctamente.', logout_response.data['message'])
