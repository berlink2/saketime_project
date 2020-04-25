import factory
import factory.fuzzy
from django.contrib.auth import get_user_model
from main import models


class UserFactory(factory.django.DjangoModelFactory):
    email = 'user1@email.com'
    username ='john'

    class Meta:
        model = get_user_model()
        django_get_or_create = ('email', 'username')


class ProductFactory(factory.django.DjangoModelFactory):
    price = factory.fuzzy.FuzzyDecimal(1.0, 1000.0, 2)

    class Meta:
        model = models.Product


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Address


class BreweryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Brewery


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Review