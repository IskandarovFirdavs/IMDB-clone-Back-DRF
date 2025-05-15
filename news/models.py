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

    def __str__(self):
        return self.title


class Trivia(models.Model):
    content = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='trivia', null=True, blank=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='trivia', null=True, blank=True)

    def __str__(self):
        return f"Trivia about {'title' if self.title else 'person'}"
