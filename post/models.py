from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    created = models.DateTimeField(editable=False)
    modeifed = models.DateTimeField()
    # slug = models.SlugField(unique=True, max_length=150, editable=False)
    slug = AutoSlugField(populate_from='title')
    image = models.ImageField(upload_to='post', null=True, blank=True)
    modeifed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='modeifed_by')

    # def get_slug(self):
    #     slug = slugify(self.title.replace('ı', 'i'))
    #     unique = slug
    #     number = 1
    #
    #     while Post.objects.filter(slug = unique).exist():
    #         # unique = '{}-{}'.format(slug, number)
    #         unique = f"{slug}-{number}"
    #         number += 1

    class Meta:
        ordering = ["-id"]

    def slugify_function(self, content):
        return content.replace('_', '-').lower()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modeifed = timezone.now()
        self.modeifed_by = self.user
        # self.slug = self.get_slug()
        return super(Post, self).save(*args, **kwargs)
