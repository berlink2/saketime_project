from django.views.generic.list import ListView
from main.models import Address
import logging
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView,UpdateView, DeleteView, FormView
from main.forms import AddressSelectionForm

# Create your views here.
logger = logging.getLogger(__name__)


class AddressListView(ListView):
    model = Address

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    fields = [
        "name",
        "address1",
        "address2",
        "zip_code",
        "city",
        "country", ]
    success_url = reverse_lazy("address_list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    fields = [
            "name",
            "address1",
            "address2",
            "zip_code",
            "city",
            "country",
        ]
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    success_url = reverse_lazy("address_list")

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class AddressSelectionView(LoginRequiredMixin, FormView):
    template_name = 'main/address_select.html'
    form_class = AddressSelectionForm
    success_url = reverse_lazy('checkout_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user']= self.request.user
        return kwargs

    def form_valid(self, form):
        del self.request.session['cart_id']
        cart = self.request.cart
        cart.create_order(
            form.cleaned_data['billing_address'],
            form.cleaned_data['shipping_address']
        )

        return super().form_valid(form)


