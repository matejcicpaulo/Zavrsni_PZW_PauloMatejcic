from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Product, Warehouse, StockItem


class WarehouseAppTests(TestCase):
    def setUp(self):
        # user za login
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # test podaci
        self.warehouse = Warehouse.objects.create(name="Skladište 1", location="Zagreb", capacity=1000)
        self.product = Product.objects.create(
            sku="SKU-0001", name="Test Proizvod", category="Test", unit_price=10.50, is_active=True
        )
        self.stock = StockItem.objects.create(
            warehouse=self.warehouse, product=self.product, quantity=5, reorder_level=2
        )

    def test_product_model_created(self):
        """Model test: product postoji i SKU je točan."""
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(self.product.sku, "SKU-0001")

    def test_products_requires_login(self):
        """View test: /products/ traži login (redirect)."""
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_logged_in_user_can_create_product(self):
        """CRUD test: ulogiran user može kreirati product."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse("product_add"), data={
            "sku": "SKU-0002",
            "name": "Novi Proizvod",
            "category": "Novo",
            "unit_price": "99.99",
            "is_active": True
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(sku="SKU-0002").exists())

    def test_search_products(self):
        """Search test: q filtrira rezultate."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("product_list") + "?q=Test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Proizvod")