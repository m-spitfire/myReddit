from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic import RedirectView
from .models import Post, Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-datePosted']


class PostDetailView(DetailView):
    model = Post


class UserPostListView(ListView):
    model = Post
    template_name = "posts/user_posts.html"
    context_object_name = 'posts'
    ordering = ['-datePosted']

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-datePosted')


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostVoteView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        user = self.request.user
        ud = self.kwargs['ud']
        url = post.get_absolute_url()
        user_up = user in post.upvoters_total.all()
        user_down = user in post.downvoters_total.all()
        if ud == 1:
            if user_up:
                post.upvoters_total.remove(user)
            elif user_down:
                post.downvoters_total.remove(user)
                post.upvoters_total.add(user)
            else:
                post.upvoters_total.add(user)
        else:
            if user_down:
                post.downvoters_total.remove(user)
            elif user_up:
                post.upvoters_total.remove(user)
                post.downvoters_total.add(user)
            else:
                post.downvoters_total.add(user)
        post.save()

        return url


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['content']

    def get_initial(self):
        initial = super().get_initial()
        obj = self.get_object()
        initial['text'] = obj.text
        return initial

    def get_success_url(self):
        post = self.object.post
        return reverse('posts:post_detail', kwargs={'pk': post.id})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['post_id'])
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        post = self.object.post
        return reverse('posts:post_detail', kwargs={'pk': post.id})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user


class CommentVoteView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        user = self.request.user
        vote = self.kwargs['ud']
        url = comment.get_absolute_url()
        change_in_upvotes = 0
        user_up = user in comment.upvoters.all()
        user_down = user in comment.downvoters.all()
        if vote == 1:
            if user_up:
                comment.upvoters.remove(user)
                change_in_upvotes = -1
            elif user_down:
                comment.downvoters.remove(user)
                comment.upvoters.add(user)
                change_in_upvotes = 2
            else:
                comment.upvoters.add(user)
                change_in_upvotes = 1
        else:
            if user_down:
                comment.downvoters.remove(user)
                change_in_upvotes = 1
            elif user_up:
                comment.upvoters.remove(user)
                comment.downvoters.add(user)
                change_in_upvotes = -2
            else:
                comment.downvoters.add(user)
                change_in_upvotes = -1
        comment.upvotes += change_in_upvotes
        comment.save()

        return url
