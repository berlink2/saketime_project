from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from main.forms import ReviewForm
from main.models import Product, Review, UserProfile
from django.contrib import messages
from .recommendation import update_clusters


def review_list(request):
    recent_reviews = Review.objects.order_by('-date')
    page = request.GET.get('page', 1)
    paginator = Paginator(recent_reviews, 5)
    try:
        reviews = paginator.page(page)
    except PageNotAnInteger:
        reviews = paginator.page(1)
    except EmptyPage:
        reviews = paginator.page(paginator.num_pages)
    context = {}
    context['recent_reviews'] = recent_reviews
    context['reviews'] = reviews
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, id):
    review = get_object_or_404(Review, id=id)
    return render(request, 'reviews/review_detail.html', {'review':review})



@login_required(login_url='login')
def add_review(request, slug):

    user= request.user
    userprofile = UserProfile.objects.get(user=user)
    sake = get_object_or_404(Product, slug=slug)
    form = ReviewForm(request.POST, instance=userprofile)

    try:
        review_check = Review.objects.get(user=userprofile, sake=sake)

    except Review.DoesNotExist:
        pass
    else:
        messages.info(request, 'You have already written a review for this sake.')
        return HttpResponseRedirect(reverse('product', args=(slug,)))


    if request.method == 'POST':
        form = ReviewForm(data=request.POST, instance=userprofile)
        if form.is_valid():
            review = Review()
            content = form.cleaned_data['content']
            rating = form.cleaned_data['rating']
            review.user = userprofile
            review.content= content
            review.rating=rating
            review.date = datetime.now()
            review.sake = sake
            review.save()
            form.save()
            update_clusters()
            messages.success(request, "Thank you for your review!")
            return HttpResponseRedirect(reverse('product', args=(slug,)))


    return render(request, 'reviews/add_review.html', {'sake':sake,'form':form})


