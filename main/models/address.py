from django.contrib.auth import get_user_model
from django.db import models


class Address(models.Model):
    SUPPORTED_COUNTRIES = (
        ("uk", "United Kingdom"),
        ("us", "United States of America"),
        ("jp", "Japan"),
        ("id", "Indonesia"),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address1 = models.CharField("Address line 1", max_length=60)
    address2 = models.CharField(
        "Address line 2", max_length=60, blank=True
    )
    zip_code = models.CharField(
        "ZIP or Postal code", max_length=12
    )
    city = models.CharField(max_length=60)
    country = models.CharField(
        max_length=3, choices=SUPPORTED_COUNTRIES
    )

    def __str__(self):
        return ", ".join(
        [
            self.name,
            self.address1,
            self.address2,
            self.zip_code,
            self.city,
            self.country,
        ])





