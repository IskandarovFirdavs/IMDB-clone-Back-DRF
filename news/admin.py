from django.contrib import admin
from .models import News, Trivia


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'author')
    search_fields = ('title', 'content')
    list_filter = ('published_at', 'author')
    autocomplete_fields = ('author', 'related_title', 'related_person')


@admin.register(Trivia)
class TriviaAdmin(admin.ModelAdmin):
    list_display = ('content', 'title', 'person')
    search_fields = ('content',)
    list_filter = ('title', 'person')
    autocomplete_fields = ('title', 'person')
