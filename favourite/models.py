from django.db import models

from django.db import models
from django.contrib.auth.models import User
from post.models import Post

# Create your models here.


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)

    def __str__(self):
        return self.user.username
