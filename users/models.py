from django.db import models

from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class UserModel(AbstractUser):
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',null=True, blank=True)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access_token': str(refresh.access_token)
        } 


class Person(models.Model):
    name = models.CharField(max_length=255)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    death_year = models.PositiveSmallIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)
    photo = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


from titles.models import Title
class TitlePerson(models.Model):

    ROLE_CHOICES = [
        ('ACTOR', 'Actor'),
        ('DIRECTOR', 'Director'),
        ('WRITER', 'Writer'),
        ('PRODUCER', 'Producer'),
        ('COMPOSER', 'Composer'),
        ('CINEMATOGRAPHER', 'Cinematographer'),
        ('EDITOR', 'Editor'),
    ]

    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='title_people')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_titles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    characters = models.JSONField(blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('title', 'person', 'role')

    def __str__(self):
        return f"{self.person.name} - {self.get_role_display()} in {self.title.primary_title}"
