from django.shortcuts import render
from main.models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class PostListView(ListView):
    model = Post
    template_name = 'news/news_list.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'news/news_post.html'