from django import forms
import logging
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.forms import (
    UserCreationForm
)
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import authenticate
from django.forms import inlineformset_factory, ModelForm
from .models import CartLine,Cart, UserProfile, Review
from datetime import datetime, date
from . import widgets
from . import models

logger = logging.getLogger(__name__)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, label="Your name")
    message = forms.CharField(
        max_length=600, widget=forms.Textarea
    )

    def send_mail(self):
        logger.info("Sending email to customer service")
        message = "From: {0}\n{1}".format(
            self.cleaned_data["name"],
            self.cleaned_data["message"],
        )

        send_mail(
            "Site message",
            message,
            "site@saketime.domain",
            ["customerservice@saketime.domain"],
            fail_silently=False,
        )


class RegistrationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("email", 'username')
        field_classes = {"email": UsernameField}

    def send_mail(self):
        logger.info(
            "Sending signup email for email=%s",
            self.cleaned_data["email"],
        )
        mail = "Welcome{}".format(self.cleaned_data["email"])
        send_mail(
            "Welcome to SakeTime",
            mail,
            "site@saketime.domain",
            [self.cleaned_data["email"]],
            fail_silently=True,
        )


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        strip=False, widget=forms.PasswordInput
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email is not None and password:
            self.user = authenticate(
            self.request, email=email, password=password
                )
            if self.user is None:
                raise forms.ValidationError(
                    "Invalid email/password combination."
                )
            logger.info(
                "Authentication successful for email=%s", email
            )
        return self.cleaned_data

    def get_user(self):
        return self.user


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user']


class UserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']
        exclude = ['user']



CartLineFormSet = inlineformset_factory(
    Cart,
    CartLine,

    fields=('quantity',),
    extra=0,
    widgets={'quantity': widgets.PlusMinusInput()}

)



class AddressSelectionForm(forms.Form):
    billing_address = forms.ModelChoiceField(
        queryset=None)
    shipping_address = forms.ModelChoiceField(
        queryset=None)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = models.Address.objects.filter(user=user)
        self.fields['billing_address'].queryset = queryset
        self.fields['shipping_address'].queryset = queryset


class ReviewForm(ModelForm):

    date = forms.DateField(widget=forms.HiddenInput(), initial=date.today, required=False)
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    content = forms.TextInput()
    lat = forms.FloatField(widget=forms.HiddenInput(), required=False)
    lng = forms.FloatField(widget=forms.HiddenInput(), required=False)
    postcode = forms.CharField(required=False)
    sake = forms

    class Meta:
        model = Review

