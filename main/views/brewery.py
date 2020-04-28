from django.shortcuts import render, redirect, render_to_response
from main.models import Brewery, Product
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib import messages

def show_brewery(request, brewery_slug):

    context = {}

    try:

        brewery = Brewery.objects.get(slug=brewery_slug)

        products = Product.objects.filter(brewery__slug=brewery_slug)

        page = request.GET.get('page', 1)
        paginator = Paginator(products, 4)
        pages= paginator.page(page)

        context['brewery'] = brewery
        context['products'] = products
        context['page_obj'] = pages

        coords = {'lat': brewery.lat, 'long': brewery.long}



    except Brewery.DoesNotExist:
        context['brewery'] = None
        messages.error(request, 'That brewery does not exist')

    return render(request, 'main/brewery_page.html', context=context)


class BreweryListView(ListView):
    template_name = "main/brewery_list.html"
    paginate_by = 5

    def get_queryset(self):
        breweries = Brewery.objects.all()

        return breweries.order_by('prefecture')