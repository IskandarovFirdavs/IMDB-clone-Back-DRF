from django.contrib import admin
from .models import Genre, Title, Episode, Review, Watchlist, Rating


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['primary_title', 'title_type', 'start_year', 'end_year', 'is_adult']
    search_fields = ['primary_title', 'original_title']
    list_filter = ['title_type', 'is_adult', 'start_year']
    filter_horizontal = ['genres']


@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['parent_series', 'season_number', 'episode_number', 'title']
    list_filter = ['parent_series', 'season_number']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'rating', 'contains_spoilers', 'created_at']
    search_fields = ['user__username', 'title__primary_title']
    list_filter = ['rating', 'contains_spoilers']


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'status', 'added_at']
    list_filter = ['status']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'score', 'rated_at']
    list_filter = ['score']
