from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from posts.forms import PostCreateForm
from posts.models import Post


# Create your views here.
class PostFeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/posts.html'


class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add_post.html'
    success_url = reverse_lazy('posts-feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Post created! Want to leave a book review?")
        return response