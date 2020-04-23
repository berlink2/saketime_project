from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from main.models import Product, ProductTag
import logging

# Create your views here.
logger = logging.getLogger(__name__)


class ProductView(DetailView):
    template_name = 'product_detail.html'
    def get_queryset(self):
        product_name = self.kwargs['slug']
        product = Product.objects.get(slug=self.slug)
        return product




class ProductListView(ListView):
    template_name = 'main/product_list.html'
    paginate_by = 4

    def get_queryset(self):

        tag = (self.kwargs['tag'])
        tags = None
        if tag != "all":
            tags = get_object_or_404(
                ProductTag, slug=tag
            )
        if tags:
            products = Product.objects.active().filter(
                tags=tags
            )
        else:
            products = Product.objects.active()
        return products.order_by("name")