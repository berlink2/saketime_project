from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from main.models import Product, ProductTag
import logging

# Create your views here.
logger = logging.getLogger(__name__)

class ProductListView(ListView):
    template_name = "main/product_list.html"
    paginate_by = 5

    def get_queryset(self):
        tag = self.kwargs["tag"]
        self.tag = None

        if tag != "all":
            self.tag = get_object_or_404(
                ProductTag, slug=tag
            )

        if self.tag:
            products = Product.objects.active().filter(
                tags=self.tag
            )
        else:
            products = Product.objects.active()

        return products.order_by("name")