from django.test import TestCase, Client
from django.core.files.base import ContentFile

from allauth.socialaccount.models import SocialApp
from unittest.mock import patch

from logapp.models import User
from ..models import ProductCategory, Customer, Favourite, Products

import pdb


class SupposeProductViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("test_user", password="admin123456")
        self.user.save()

    def test_succesful_redirect(self):
        with self.assertRaises(SocialApp.DoesNotExist):
            resp = self.client.get("/shop/create_product")
            self.assertRedirects(resp, "/logpage/")

        logged_in = self.client.login(username="test_user", password="admin123456")
        self.assertTrue(logged_in)

        resp2 = self.client.get("/shop/create_product")
        self.assertEqual(resp2.status_code, 200)
        self.assertTemplateUsed(resp2, "shop/product-create_page.html")

    @patch("captcha.fields.CaptchaField.clean")
    def test_product_created(self, mock_validate):

        test_category = ProductCategory.objects.create(name="TEST_CATEGORY")
        png_header = (b"\x89PNG\r\n\x1a\n", b"\x00\x00\x00\rIHDR")  # minimal header
        test_image = ContentFile("img1.png", png_header)
        Customer.objects.create(user=self.user, name="Test User", email="")
        Favourite.objects.create(customer=self.user.customer)

        mock_validate.return_value = True
        self.client.force_login(self.user)

        resp = self.client.get("/shop/create_product")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "shop/product-create_page.html")

        resp2 = self.client.post(
            "/shop/create_product",
            {
                "name": "Test Product",
                "description": "This is a test product.",
                "images": [
                    test_image,
                ],
                "quantity": 10,
                "price": 99.99,
                "service": False,
                "categories": [
                    test_category.id,
                ],
                "captcha": "",
            },
            follow=True,
        )
        mock_validate.assert_called_once()
        self.assertRedirects(resp2, "/shop/")

        created_product = Products.objects.get(name="Test Product")
        self.assertEqual(created_product.ontest, True)
        self.assertEqual(created_product.service, False)
        self.assertTrue(
            created_product.categories.filter(name="TEST_CATEGORY").exists()
        )
