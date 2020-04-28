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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products_name_order = Product.objects.active().order_by('name')
        products_price_order = Product.objects.active().order_by('price')
        products_brewery = Product.objects.active().order_by('brewery')
        products_units_sold = Product.objects.active().order_by('units_sold')
        context['products_name_order'] = products_name_order
        context['products_price_order'] = products_price_order
        context['products_brewery'] = products_brewery
        context['products_units_sold'] = products_units_sold

        return context

    def get_queryset(self):
        tag = self.kwargs["tag"]
        self.tag = None

        sorts = ['name', 'price', 'units_sold']

        if tag in sorts:
            products = Product.objects.active().order_by(tag)
            return products


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


        return products.order_by()




