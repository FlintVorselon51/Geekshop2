from django.conf import settings
from django.test import TestCase
from django.test import Client

from authapp.models import ShopUser


class UserManagementTestCase(TestCase):

    success_code = 200
    redirect_code = 302

    username = 'django'
    email = 'django@gb.local'
    password = 'admin'

    new_user_data = {
        'username': 'django1',
        'first_name': 'Django',
        'last_name': 'Django',
        'password1': 'STRONG_password666',
        'password2': 'STRONG_password666',
        'age': 18,
        'email': 'django1@gb.local'
    }

    def setUp(self) -> None:

        self.user = ShopUser.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.success_code)
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.redirect_code)

    def test_user_register(self):
        response = self.client.post('/auth/register/', data=self.new_user_data)
        self.assertEqual(response.status_code, self.redirect_code)

        new_user = ShopUser.objects.get(username=self.new_user_data['username'])
        activation_url = f'{settings.DOMAIN_NAME}/auth/verify/{new_user.email}/{new_user.activation_key}/'

        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.success_code)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

    def test_logout(self):
        self.test_login()

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
