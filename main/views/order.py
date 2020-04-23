from django.contrib.auth.mixins import UserPassesTestMixin
from django import forms as django_forms
from django.db import models as django_models
import django_filters
from django_filters.views import FilterView
from django.urls import reverse_lazy
from main.models import Order


class DateInput(django_forms.DateInput):
    input_type = 'date'


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = {
            'user__email': ['icontains'],
            'status': ['exact'],
            'date_updated': ['gt', 'lt'],
            'date_added': ['gt', 'lt'],
        }
        filter_overrides = {
            django_models.DateTimeField: {
                'filter_class': django_filters.DateFilter, 'extra': lambda f: {
                    'widget': DateInput}
            }
        }


class OrderView(UserPassesTestMixin, FilterView):
    filterset_class = OrderFilter
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_staff is True


