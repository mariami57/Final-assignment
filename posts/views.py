from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from books.models import Book
from common.mixins import UserIsCreatorMixin
from destinations.models import Destination
from posts.forms import PostCreateForm, PostEditForm
from posts.models import Post


# Create your views here.
class PostFeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/posts.html'

class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add-post.html'
    success_url = reverse_lazy('posts-feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        book_choice = form.cleaned_data.get('book_choice')
        book_title = form.cleaned_data.get('book_title')

        dest_choice = form.cleaned_data.get('destination_choice')
        dest_name = form.cleaned_data.get('destination_name')

        if book_choice == 'other' and book_title:
            book = Book.objects.create(
                title=book_title,author="Unknown", added_by=self.request.user,)
        else:
            book = Book.objects.get(id=book_choice)

        if dest_choice == 'other' and dest_name:
            d_name, d_country = dest_name.split(',')
            destination = Destination.objects.create(
                name=d_name,
                country=d_country,
                )
        else:
            destination = Destination.objects.get(id=dest_choice)

        form.instance.book = book
        form.instance.destination = destination
        if book and destination:
            book.destinations.add(destination)

        response = super().form_valid(form)

        messages.success(self.request, 'Post created! Want to leave a book review?')
        return response

class PostEditView(LoginRequiredMixin, UserIsCreatorMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'posts/edit-post.html'
    success_url = reverse_lazy('posts-feed')

@login_required
def post_delete_view(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user.pk == post.user.pk:
        post.delete()
        return redirect('posts-feed')
    else:
        return HttpResponseForbidden()
