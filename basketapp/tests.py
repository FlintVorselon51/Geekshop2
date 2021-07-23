from django.test import TestCase
from django.test import Client
from django.conf import settings

from authapp.models import ShopUser
from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


class UserManagementTestCase(TestCase):

    success_code = 200
    redirect_code = 302

    username = 'django'
    email = 'django@gb.local'
    password = 'admin'

    category_data = {
        'name': 'стулья'
    }

    products_data = [
        {'name': 'стул_1', 'price': 1000},
        {'name': 'стул_2', 'price': 3000},
        {'name': 'стул_3', 'price': 2500}
    ]

    def setUp(self) -> None:

        self.user = ShopUser.objects.create_superuser(self.username, email=self.email, password=self.password)
        self.category = ProductCategory.objects.create(**self.category_data)
        self.products = [Product.objects.create(category=self.category, **data) for data in self.products_data]

        self.client = Client()

    def test_create(self):
        basket_items = [Basket.objects.create(user=self.user, product=product) for product in self.products]
        # ???
        self.assertEqual(list(Basket.objects.filter(user=self.user)), basket_items)
        self.assertEqual([basket.product for basket in basket_items], self.products)
