from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    UserPostListView,
    PostCreateView,
    PostDeleteView,
    PostUpdateView,
    CommentCreateView,
    CommentEditView,
    CommentDeleteView
)

app_name = 'posts'

urlpatterns = [
    path('',PostListView.as_view(),name='posts_home'),
    path('posts/<int:pk>/',PostDetailView.as_view(),name='post_detail'),
    path('user/<str:username>/', UserPostListView.as_view(),name='user_posts'),
    path('post/new/',PostCreateView.as_view(),name='post_create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(),name='post_delete'),
    path('post/<int:post_id>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:post_id>/comment/edit/<int:pk>/', CommentEditView.as_view(), name='comment_edit'),
    path('post/<int:post_id>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
]