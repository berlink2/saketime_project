from django.test import TestCase
from main import models
from main import factories
from django.contrib.auth import get_user_model


class TestModel(TestCase):

    def test_active_manager_works(self):
        factories.ProductFactory.create_batch(2, active=True)
        factories.ProductFactory(active=False)
        self.assertEqual(len(models.Product.objects.active()), 2)

    def test_username(self):
        user1 = get_user_model().objects.create_user('user@email.com',"pw432joij")
        user1.username = 'john'
        self.assertEqual('john', user1.username)


    def test_create_order_works(self):
        p1 = factories.ProductFactory()
        p2 = factories.ProductFactory()
        user1 = factories.UserFactory()

        billing = factories.AddressFactory(user=user1)
        shipping = factories.AddressFactory(user=user1)

        cart = models.Cart.objects.create(user=user1)
        models.CartLine.objects.create(
            cart=cart, product=p1
        )
        models.CartLine.objects.create(
            cart=cart, product=p2
        )

        with self.assertLogs("main.models.cart", level="INFO") as cm:
            order = cart.create_order(billing, shipping)
        self.assertGreaterEqual(len(cm.output), 1)
        order.refresh_from_db()
        self.assertEquals(order.user, user1)
        self.assertEquals(
            order.billing_address1, billing.address1
        )
        self.assertEquals(
            order.shipping_address1, shipping.address1
        )
        # add more checks here
        self.assertEquals(order.lines.all().count(), 2)
        lines = order.lines.all()
        self.assertEquals(lines[0].product, p1)
        self.assertEquals(lines[1].product, p2)