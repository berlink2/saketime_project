from django.urls import include,path
from django.views.generic import TemplateView, DetailView
from .views import ContactUsView, ProductListView, RegisterView, logout_user, add_to_cart, manage_cart, order
from .models.product import Product
from main import forms, views
from django.contrib.auth import views as auth_views
from django.conf.urls import url


urlpatterns = [
    path("about-us/",TemplateView.as_view(template_name="about_us.html"),name='about-us'),
    path('contact-us/', ContactUsView.as_view(),name='contact-us'),
    path('', TemplateView.as_view(template_name='home.html'),name='home'),
    path('product/<slug:slug>/', DetailView.as_view(model=Product), name='product'),
    path('products/<slug:tag>/', ProductListView.as_view(), name='product-list'),
    #path('products/all', TemplateView.as_view(template_name='main/product_list.html'),name='all'),

    path('register/', RegisterView.as_view(), name='register'),
    path("login/", auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name="login.html", form_class=forms.AuthenticationForm), name="login",),
    path('logout/', logout_user, name='logout'),
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
    path('add_to_cart/', add_to_cart, name='add-to-cart'),
    path('cart/', manage_cart, name='cart' ),
    path("order/done/", TemplateView.as_view(template_name="main/order_done.html"), name="checkout_done",),
    path("order/address_select/",views.AddressSelectionView.as_view(),name="address_select",),
    path('order-dashboard', views.OrderView.as_view(), name='order_dashboard'),

]
