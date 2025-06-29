from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from posts.forms import PostCreateForm
from posts.models import Post


# Create your views here.
class PostFeedView(ListView):
    model = Post
    template_name = 'posts/posts.html'


class AddPostView(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add_post.html'
    success_url = reverse_lazy('posts-feed')
