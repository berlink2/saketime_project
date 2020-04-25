import sys, os, django, json, random
from main.models import Brewery, Product
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saketime_project.settings')
django.setup()
random.seed(8765)


def populate_breweries():
    print('populating breweries')
    breweries = []
    with open('main/data/breweries.json') as f:
        breweries = json.load(f)

        for data in breweries:
            brewery_results =[]
            try:
                brewery_results = Brewery.objects.get(name=data['name'])
            except Brewery.DoesNotExist:
                pass

            if not brewery_results:
                brewery = Brewery()
                brewery.name = data['name']
                brewery.address = data['address']
                brewery.phone = data['phone']
                brewery.email = data['email']
                brewery.description = data['description']
                brewery.image = data['image']
                brewery.lat = data['lat']
                brewery.long = data['long']
                brewery.website = data['website']

                brewery.save()

#
# def populate_products():
#     print('populating products')
#
#
#     products =[]
#
#     with open('main/data/products.json') as f:
#         json.load(f)
#
#         for data in products:
#             product, created = Product.objects.get_or_create(name=data['name'])
#
#             if created:
#                 tags = data['tags'].split(',')
#                 for tag_name in tags:
#                     if tag_name != '':
#                         tag_name = tag_name.title()
#
#
