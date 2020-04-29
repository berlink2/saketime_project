from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from main.models import Review, Cluster, Product, UserProfile
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np


@login_required(login_url='login')
def user_recommend_list(request):
    userprofile = UserProfile.objects.get(user=request.user)

    user_reviews = Review.objects.filter(user=userprofile).prefetch_related('sake')
    reviewed_sakes = set(map(lambda x:x.sake.id, user_reviews))

    try:
        user_cluster_name = UserProfile.objects.get(id=userprofile.id).cluster_set.first().name
    except AttributeError:
        update_clusters(is_new_user=True)
        user_cluster_name = UserProfile.objects.get(id=userprofile.id).cluster_set.first().name

    user_cluster_other_members = Cluster.objects.get(name=user_cluster_name).users.exclude(id=userprofile.id).all()

    other_member_id = set([x.id for x in user_cluster_other_members])

    other_users_reviews = Review.objects.filter(user_id__in=other_member_id).exclude(
        sake__id__in=reviewed_sakes
    )
    other_users_reviews_sake_ids = set(map(lambda x: x.sake.id, other_users_reviews))

    sake_list = sorted(
        list(Product.objects.filter(id__in=other_users_reviews_sake_ids)),
        key=Product.average_rating,
        reverse=True
    )

    context = {}
    context['sake_list'] = sake_list

    page = request.GET.get('page', 1)
    paginator = Paginator(sake_list, 5)
    try:
        suggestions = paginator.page(page)
    except PageNotAnInteger:
        suggestions = paginator.page(1)
    except EmptyPage:
        suggestions = paginator.page(paginator.num_pages)
    context['suggestions'] = suggestions
    return render(request, 'recommendations/user_recommendation_list.html', context)


def update_clusters(is_new_user):
    num_reviews = Review.objects.count()
    update_step = ((num_reviews/100)+1) * 5
    if num_reviews % update_step == 0 or is_new_user:
        #all_user_ids = map(lambda x: x.id, UserProfile.objects.only("user_id"))
        all_user_ids = [x.id for x in UserProfile.objects.only('user_id')]
        all_sake_ids = set(map(lambda x: x.sake.id, Review.objects.only("sake")))
        #num_users = len(all_user_ids)
        num_users = 0
        for i in all_user_ids:
            num_users +=1

        ratings_m = dok_matrix((num_users, max(all_sake_ids)+1), dtype=np.float32)
        for i in range(num_users):  # each user corresponds to a row, in the order of all_user_names
            user_reviews = Review.objects.filter(user_id=all_user_ids[i])
            for user_review in user_reviews:
                ratings_m[i, user_review.sake.id] = user_review.rating

        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())

        Cluster.objects.all().delete()

        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values():
            cluster.save()
        for i, cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(UserProfile.objects.get(id=all_user_ids[i]))








