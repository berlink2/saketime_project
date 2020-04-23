from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from main import forms
import logging
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
logger = logging.getLogger(__name__)


class RegisterView(UserPassesTestMixin, FormView):
    template_name = "register.html"
    form_class = forms.RegistrationForm
    login_url = reverse_lazy('home')
    model = get_user_model()

    def test_func(self):
        return self.request.user.is_anonymous is True

    def handle_no_permission(self):
        return redirect('home')

    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        email = form.cleaned_data.get("email")
        username = form.cleaned_data.get('username')
        user.username = username
        user.save()
        raw_password = form.cleaned_data.get("password1")
        logger.info(
            "New signup for email=%s through RegisterView", email
        )

        user = authenticate(email=email, password=raw_password,)
        login(self.request, user)
        form.send_mail()
        messages.info(
            self.request, "You signed up successfully."
        )
        return response