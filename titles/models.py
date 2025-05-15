from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    TYPE_CHOICES = [
        ('MOVIE', 'Movie'),
        ('TV_SERIES', 'TV Series'),
        ('TV_EPISODE', 'TV Episode'),
        ('VIDEO_GAME', 'Video Game'),
        ('SHORT', 'Short'),
        ('TV_MINI_SERIES', 'TV Mini Series'),
        ('TV_SPECIAL', 'TV Special'),
        ('VIDEO', 'Video'),
    ]

    title_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    primary_title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    is_adult = models.BooleanField(default=False)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    runtime_minutes = models.PositiveIntegerField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    poster = models.URLField(blank=True)
    plot = models.TextField(blank=True)
    average_rating = models.FloatField(null=True, blank=True)
    num_votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.primary_title} ({self.start_year})"


class Episode(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='episodes')
    season_number = models.PositiveSmallIntegerField()
    episode_number = models.PositiveSmallIntegerField()
    parent_series = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='series_episodes')

    class Meta:
        unique_together = ('parent_series', 'season_number', 'episode_number')

    def __str__(self):
        return f"{self.parent_series.primary_title} S{self.season_number}E{self.episode_number}: {self.title.primary_title}"


from users.models import UserModel
class Review(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 11)])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contains_spoilers = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return f"{self.user.username}'s review of {self.title.primary_title}"


class Watchlist(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='watchlists')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='in_watchlists')
    added_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ('PLAN_TO_WATCH', 'Plan to Watch'),
        ('WATCHING', 'Watching'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLAN_TO_WATCH')

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return f"{self.user.username}'s watchlist item: {self.title.primary_title}"


class Rating(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='ratings')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 11)])
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return f"{self.user.username} rated {self.title.primary_title} {self.score}/10"
