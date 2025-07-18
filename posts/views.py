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
        if book_choice:
            book = Book.objects.get(id=book_choice)
            form.instance.book = book
        else:

            form.add_error('book_choice', 'Please select a book.')
            return self.form_invalid(form)

        dest_choice = form.cleaned_data.get('destination_choice')
        if dest_choice:
            destination = Destination.objects.get(id=dest_choice)
            form.instance.destination = destination
        else:
            form.add_error('destination_choice', 'Please select a destination.')
            return self.form_invalid(form)


        response = super().form_valid(form)

        if book and destination:
            book.destinations.add(destination)

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
