from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.models import UserProfile



class UserProfileView(DetailView, LoginRequiredMixin):
    template_name = 'main/userprofile.html'
    model = UserProfile












