from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField 
from PIL import Image

def get_deleted_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.SET(get_deleted_user))
    datePosted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail',kwargs={'pk':self.pk})


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET(get_deleted_user))
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} with id {self.pk}"

    def get_absolute_url(self):
        return reverse('posts:post_detail',kwargs={'pk':self.post.id})