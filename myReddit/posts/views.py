from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

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
    

class CommentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(id=self.kwargs['post_id'])
        return super().form_valid(form)
    
    def test_func(self):
        return True

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']

    def get_initial(self):
        initial = super().get_initial()
        obj = self.get_object()
        initial['text'] = obj.text
        return initial

    def get_success_url(self):
        post = self.object.post
        return reverse('posts:post_detail', kwargs={'pk':post.id})

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
        return reverse('posts:post_detail',kwargs={'pk':post.id})

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user