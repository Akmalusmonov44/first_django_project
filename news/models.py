
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

class PublishedManagers(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
# Create your models here.
class News(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'PB', 'Published'
    # id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.Draft)


    objects = models.Manager()
    published = PublishedManagers()

    class Meta:
        ordering = ['-publish_time']
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse( 'news_details_page', args=[self.slug])

class Comment(models.Model):
    news = models.ForeignKey('News',
                             on_delete=models.CASCADE,
                             related_name='comments')

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments')

    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return f"Comment - {self.body} by {self.user}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.email


