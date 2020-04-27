from django.shortcuts import render, redirect, render_to_response
from main.models import Brewery, Product


def show_bestseller(request):
    context ={}
    breweries = Brewery.objects.all()
    products = Product.objects.order_by('units_sold')
    context['best_product'] = products[0]

    most_sales = 0
    bestseller = None

    for brewery in breweries:
        most_sales = max(most_sales, brewery.get_total_sales())

    for brewery in breweries:
        if brewery.get_total_sales() == most_sales:
            bestseller = brewery
            context['best_brewery'] = bestseller

    return render(request, 'home.html', context)

