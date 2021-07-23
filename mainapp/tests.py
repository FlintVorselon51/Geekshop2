from django.test import TestCase
from django.test.client import Client

from mainapp.models import ProductCategory, Product


class TestMainSmokeTest(TestCase):

    success_code = 200

    def setUp(self) -> None:
        cat_1 = ProductCategory.objects.create(
            name='cat_1'
        )

        Product.objects.create(
            category=cat_1,
            name='prod_1'
        )

        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.success_code)

    def test_products_urls(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/product/{product_item.pk}/')
            self.assertEqual(response.status_code, self.success_code)
