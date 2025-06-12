from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import Products, ProductCategory, Customer, ProductOffers
from logapp.models import User


class ProductsModelTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.TEST_USER = User.objects.create(username="testuser", email="")
        cls.TEST_CUSTOMER = Customer.objects.create(
            user=cls.TEST_USER, name="Test User", email=""
        )
        cls.TEST_PRODUCT = Products.objects.create(
            name="Test Product",
            description="This is a test product.",
            quantity=10,
            price=99.99,
            seller=cls.TEST_USER,
            service=False,
        )

    def test_product_correctly_identified(self):
        product = Products.objects.get(name="Test Product")
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "This is a test product.")
        self.assertEqual(product.quantity, 10)
        self.assertEqual(product.price, 99.99)
        self.assertFalse(product.service)
        self.assertIsNotNone(product.seller)

    def test_productoffer_initiatlized_from_product(self):
        product = Products.objects.get(name="Test Product")
        offer = ProductOffers.objects.initialize_offer(product)
        self.assertIsNotNone(offer)
        self.assertEqual(offer.product, product)
        self.assertEqual(offer.price, product.price)
        self.assertEqual(offer.availability, product.quantity)
        self.assertEqual(offer.owner, product.seller.customer)

        self.assertFalse(offer.is_active)

    def test_product_price_validation(self):
        product = Products.objects.get(name="Test Product")
        product.price = product.price - 10.0
        self.assertEqual(product.price, 89.99)
        with self.assertRaises(ValidationError):
            product.price = -1.0
            product.full_clean()

    def test_product_quantity_validation(self):
        product = Products.objects.get(name="Test Product")
        with self.assertRaises(ValidationError):
            product.quantity = -1
            product.full_clean()
