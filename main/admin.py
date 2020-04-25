from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.db.models.functions import TruncDay
from django.db.models import Avg, Count, Min, Sum
from django.urls import path
from django.template.response import TemplateResponse
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


# Register your models here.

def make_active(self, request, queryset):
    queryset.update(active=True)


make_active_description = 'Mark selected items as active'


def make_inactive(self,request, queryset):
    queryset.update(active=False)


make_active_description = 'Mark selected items as inactive'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'in_stock', 'price')
    list_filter = ('active', 'in_stock', 'date_updated')
    list_editable = ('in_stock',)
    autocomplete_fields = ('tags',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    actions =  [make_active, make_inactive]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ['slug', 'name']

    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}


admin.site.register(Product, ProductAdmin)


class DispatchersProductAdmin(ProductAdmin):
    readonly_fields = ('description', 'price', 'tags', 'active')
    prepopulated_fields = {}
    autocomplete_fields = ()


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('active',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.readonly_fields
        return list(self.readonly_fields) + ["slug", "name"]

    def get_prepopulated_fields(self, request, obj=None):
        if request.user.is_superuser:
            return self.prepopulated_fields
        else:
            return {}


admin.site.register(ProductTag, ProductTagAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'image', 'product_name',)
    search_fields = ('product_name', 'product__name',)

    def image_tag(self, obj):
        if obj.image:
            #image_url = obj.image.url
            return obj.image.url
            #return format_html('<img src="%s"/>' % obj.image.url)
            #return format_html(f'<img src="{image_url}"/>')
        return '-'

    def product_name(self, obj):
        return obj.product.name


admin.site.register(ProductImage, ProductImageAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'address1', 'address2', 'zip_code', 'city', 'country')
    list_filter = ('city', 'country')
    readonly_fields = ('user',)


admin.site.register(Address, AddressAdmin)


class CartLineInline(admin.TabularInline):
    model = CartLine
    raw_id_fields = ('product',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'count')
    list_editable = ('status',)
    list_filter = ('status',)
    inlines = (CartLineInline,)


@admin.register(CartLine)
class CartLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    raw_id_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status")
    list_editable = ("status",)
    list_filter = ("status", "shipping_country", "date_added")
    inlines = (OrderLineInline,)
    fieldsets = (
        (None, {"fields": ("user", "status")}),
        (
            "Billing info",
            {
                "fields": (
                    "billing_name",
                    "billing_address1",
                    "billing_address2",
                    "billing_zip_code",
                    "billing_city",
                    "billing_country",
                )
            },
        ),
        (
            "Shipping info",
            {
                "fields": (
                    "shipping_name",
                    "shipping_address1",
                    "shipping_address2",
                    "shipping_zip_code",
                    "shipping_city",
                    "shipping_country",
                )
            },
        ),
    )


admin.site.register(Brewery)
admin.site.register(UserProfile)
admin.site.register(Review)




