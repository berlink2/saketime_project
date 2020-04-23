from django.contrib import auth
from django.urls import reverse
from main import models
from django.contrib.auth import get_user_model
from decimal import Decimal


def test_merge_carts(self):
    user1 = get_user_model().objects.create_user(
        "user1@amazing.com", "g45g43h3rg35g"
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
    cart = models.Cart.objects.create(user=user1)
    models.CartLine.objects.create(
        cart=cart,product=test_product,quantity=2
    )
    response = self.client.get(
        reverse("add_to_basket"), {"product_id": test_product2.id}
    )
    response = self.client.post(
        reverse("login"),
        {"email": "user1@amazing.com", "password": "g45g43h3rg35g"},
    )
    self.assertTrue(
        auth.get_user(self.client).is_authenticated
    )
    self.assertTrue(
        models.Cart.objects.filter(user=user1).exists()
    )
    cart = models.Cart.objects.get(user=user1)
    self.assertEquals(cart.count(), 3)


