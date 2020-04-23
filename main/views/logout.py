from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out')
    return redirect('home')
