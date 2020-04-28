from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from main.models import UserProfile
from main.forms import UserProfileForm,UserForm
from django.views.generic.edit import UpdateView


class UserProfileView(DetailView, LoginRequiredMixin):
    template_name = 'main/userprofile.html'
    model = UserProfile

@login_required(login_url='login')
def account_settings(request):
    user = request.user
    userprofile = UserProfile.objects.get(user=user)
    userprofileform = UserProfileForm(instance=user)
    userform = UserForm(instance=user)

    if request.method == 'POST':
        userprofileform = UserProfileForm(data=request.POST, files=request.FILES,  instance=userprofile)
        userform = UserForm(request.POST, instance=user)
        if userform.is_valid() and userprofileform.is_valid():

            userprofileform.save()
            userform.save()

            return HttpResponseRedirect(reverse('settings'))

    context = {'userprofileform': userprofileform, 'userform':userform}
    return render(request, 'accounts/account_settings.html', context)














