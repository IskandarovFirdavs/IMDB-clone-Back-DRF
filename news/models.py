from django.db import models
from titles.models import Title
from users.models import UserModel, Person


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    related_title = models.ForeignKey(Title, on_delete=models.SET_NULL, null=True, blank=True)
    related_person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='news_images/', null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255)
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-published_at']
        verbose_name_plural = 'News'


class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Trivia(models.Model):
    content = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='trivia', null=True, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='trivia', null=True, blank=True)
    verified = models.BooleanField(default=False)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-upvotes']