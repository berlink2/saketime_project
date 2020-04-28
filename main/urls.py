from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView, DetailView
from .views import (ContactUsView, ProductListView, RegisterView,
    logout_user, add_to_cart, show_bestseller, BreweryListView, add_review,
    account_settings, manage_cart, remove_one_from_cart, add_one_to_cart,
    review_detail, review_list, show_brewery, UserProfileView,remove_product_from_cart)

from .models.product import Product
from main import forms, views, endpoints
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'orderlines', endpoints.PaidOrderLineViewSet)
router.register(r'orders', endpoints.PaidOrderViewSet)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("about-us/",TemplateView.as_view(template_name="about_us.html"),name='about-us'),
    path('contact-us/', ContactUsView.as_view(),name='contact-us'),
    path('', show_bestseller,name='home'),
    path('add_to_cart/', add_to_cart, name='add-to-cart'),
    path('cart/', manage_cart, name='cart'),
    path('remove/<slug:slug>', remove_product_from_cart, name='remove-product-from-cart' ),
    path('add_one_to_cart/<slug:slug>', add_one_to_cart, name='add-one-to-cart' ),
    path('remove_one_from_cart/<slug:slug>', remove_one_from_cart, name='remove-one-from-cart' ),
    path('brewery/<slug:brewery_slug>/', show_brewery, name='brewery'),
    path('breweries/', BreweryListView.as_view(), name='breweries'),
    path('product/<slug:slug>/', DetailView.as_view(model=Product), name='product'),
    path('products/<slug:tag>/', ProductListView.as_view(), name='product-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="login.html", form_class=forms.AuthenticationForm), name="login",),
    path('logout/', logout_user, name='logout'),
    path('user/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('settings/', account_settings, name='settings'),
    path(
            "address/",
            views.AddressListView.as_view(),
            name="address_list",
    ), path(
           "address/create/",
            views.AddressCreateView.as_view(),
            name="address_create",
    ), path(
           "address/<int:pk>/",
           views.AddressUpdateView.as_view(),
           name="address_update",
    ), path(
           "address/<int:pk>/delete/",
           views.AddressDeleteView.as_view(),
           name="address_delete",
    ),
    path("order/done/", TemplateView.as_view(template_name="main/order_done.html"), name="checkout_done",),
    path("order/address_select/",views.AddressSelectionView.as_view(),name="address_select",),
    path('order-dashboard', views.OrderView.as_view(), name='order_dashboard'),
    path('reviews/<int:id>', review_detail, name='review_detail'),
    path('reviews/',review_list,name='review_list'),

    path('product/<slug:slug>/add_review/', add_review, name='add_review'),
    path('api/', include(router.urls)),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

