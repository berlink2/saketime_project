from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.contrib import auth
from django.contrib.auth import get_user_model
from main import models
# Create your tests here.



class TestPage(TestCase):
    def test_home_page_works(self):
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_about_us_page_works(self):
        response = self.client.get(reverse("about-us"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about_us.html')


    def test_user_signup_page_loads_correctly(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")


    def test_address_list_page_returns_only_owned(self):
        user1 = get_user_model().objects.create_user(
        "user1", "pw432joij"
    )

        user2 = get_user_model().objects.create_user(
            "user2", "pw432joij"
        )
        models.Address.objects.create(
            user=user1,
            name="john kimball",
            address1="flat 2",
            address2="12 Stralz avenue",
            city="London",
            country="uk",
        )
        models.Address.objects.create(
            user=user2,
            name="marc kimball",
            address1="123 Deacon road",
            city="Los Angeles",
            country="us",
        )
        self.client.force_login(user2)
        response = self.client.get(reverse("address_list"))
        self.assertEqual(response.status_code, 200)

        address_list = models.Address.objects.filter(user=user2)
        self.assertEqual(
            list(response.context["object_list"]),
            list(address_list),)

    def test_address_create_stores_user(self):
        user1 = get_user_model().objects.create_user("user1", "pw432joij")

        post_data = {
            "name": "john kercher",
            "address1": "1 av st",
            "address2": "",
            "zip_code": "MA12GS",
            "city": "Manchester",
            "country": "uk",
        }

        self.client.force_login(user1)
        self.client.post(
            reverse("address_create"), post_data
        )
        self.assertTrue(
            models.Address.objects.filter(user=user1).exists()
        )

    def test_add_to_cart(self):
        user1 = get_user_model().objects.create_user(
           'user1', 'pw432join'
        )

        test_product = models.Product.objects.create(
            name="okini okini",
            slug="okini-okini",
            price=Decimal("10.00"),
        )
        test_product2 = models.Product.objects.create(
            name="nice nice",
            slug="nice-nice",
            price=Decimal("12.00"),
        )

        self.client.force_login(user1)

        response = self.client.get(reverse("add-to-cart"), {"product_id": test_product.id})
        response = self.client.get(reverse("add-to-cart"), {"product_id": test_product.id})

        self.assertEquals(models.CartLine.objects.filter(cart__user=user1).count(),1)

        response = self.client.get(reverse("add-to-cart"), {"product_id": test_product2.id})

        self.assertEquals(models.CartLine.objects.filter(cart__user=user1).count(),2)
