from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView


from common.mixins import UserIsCreatorMixin
from posts.forms import PostCreateForm, PostEditForm
from posts.mixins import BookDestinationHandlerMixin
from posts.models import Post


# Create your views here.
class PostFeedView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/posts.html'

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_at')

        return queryset


class AddPostView(BookDestinationHandlerMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/add-post.html'
    success_url = reverse_lazy('posts-feed')

    def form_valid(self, form):
        form.instance.user = self.request.user
        book, destination = self.handle_book_and_destination(form)
        form.instance.book = book
        form.instance.destination = destination
        super().form_valid(form)

        messages.success(self.request, 'Post created! Want to leave a book review?')
        print(form.errors)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("FORM INVALID")
        print(form.errors)
        return super().form_invalid(form)

class PostEditView(LoginRequiredMixin, UserIsCreatorMixin, UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'posts/edit-post.html'
    success_url = reverse_lazy('posts-feed')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_object()
        kwargs['request'] = self.request
        return kwargs

@login_required
def post_delete_view(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user.pk == post.user.pk:
        post.delete()
        return redirect('posts-feed')
    else:
        return HttpResponseForbidden()

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post-detail.html'

