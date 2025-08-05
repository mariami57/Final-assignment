from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views.generic.edit import FormMixin

from comments.forms import CommentBaseForm
from comments.models import Comment
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

        return super().form_valid(form)


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
        return HttpResponseForbidden("You are not allowed to delete this post.")

class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = 'posts/post-detail.html'
    form_class = CommentBaseForm

    def get_success_url(self):
        return reverse('post-details', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()

        context['comments'] = Comment.objects.filter(
            post=post)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = self.request.user
            comment.post = self.object
            comment.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)





